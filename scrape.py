#!/var/www/html/wsgi/flask/bin/python3
# -*- coding: utf-8 -*-
#import mechanize
#import http.cookiejar as cookielib
import codecs
from bs4 import BeautifulSoup
from math import ceil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Scraper():

    def __init__(self):
        # self.br = mechanize.Browser()
        # cj = cookielib.LWPCookieJar()
        # self.br.set_cookiejar(cj)
        # # Browser options
        # self.br.set_handle_equiv(True)
        # self.br.set_handle_gzip(True)
        # self.br.set_handle_redirect(True)
        # self.br.set_handle_referer(True)
        # self.br.set_handle_robots(False)
        # self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        # self.br.addheaders = [('User-agent', 'Chrome')]
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)


    def login(self):           
        # self.br.open('https://www.filmweb.pl/login')
        # self.br.select_form(nr=1)
        # # User credentials stored in file not visible outside server
        # with open('/var/www/html/hidden/pass', 'r') as pass_file:
        #     self.br.form['j_username'] = pass_file.readline().rstrip()
        #     self.br.form['j_password'] = pass_file.readline().rstrip()
        # # Login
        # self.br.submit()
        self.driver.get('https://filmweb.pl/login')
        self.driver.find_element_by_class_name('fwBtn--gold').click()
        self.driver.find_element_by_class_name('authButton--filmweb').click()
        with open('/var/www/html/hidden/pass', 'r') as pass_file:
            self.driver.find_element_by_name('j_username').send_keys(pass_file.readline().rstrip())
            self.driver.find_element_by_name('j_password').send_keys(pass_file.readline().rstrip())
        self.driver.find_element_by_class_name('materialForm__submit').click()



    def get_ratings_page(self, username, page_no):
        page = self.open_page('https://www.filmweb.pl/user/'+username+'/films?page='+str(page_no))
        # Fix for unicode chars
        page = codecs.escape_decode(bytes(page,"utf-8"))[0].decode("utf-8")
        return page

    def open_page(self, url):
        #page = self.br.open(url)
        #page = str(page.get_data())
        self.driver.get(url)
        return self.driver.page_source

    def get_number_of_ratings(self, username):
        page = self.open_page('https://www.filmweb.pl/user/'+username+'/films')
        soup = BeautifulSoup(page)
        ratings_number = soup.find('span', class_='blockHeader__titleInfoCount')
        if ratings_number is None:
            print('Parsing page failed.')
            return None
        return int(ratings_number.text)

    def get_titles_from_page(self, page):
        soup = BeautifulSoup(page)
        titles = soup.find_all('h3', class_='filmPreview__title')
        if titles is not None:
            titles = [title.get_text() for title in titles]
            return titles
        return None

    #TODO Remove duplication
    def get_ratings_from_page(self, page):
        soup = BeautifulSoup(page)
        ratings = soup.find_all('span', class_='userRate__rate')
        if ratings is not None:
            ratings = [rating.get_text() for rating in ratings]
            return ratings
        return None
    
    def get_production_years_from_page(self, page):
        soup = BeautifulSoup(page)
        years = soup.find_all('span', class_='filmPreview__year')
        if years is not None:
            years = [year.get_text() for year in years]
            return years
        return None

    def get_watch_dates_from_page(self, page):
        soup = BeautifulSoup(page)
        divs = soup.find_all('div', class_='voteCommentBox__date')
        if divs is not None:
            dates = [div.a.get_text() for div in divs]
            return dates
        return None

    def calculate_number_of_pages(self, username):
        ratings_no = self.get_number_of_ratings(username)
        if ratings_no is None:
            return None
        pages_no = ceil(ratings_no/25.0) # 25 ratings per page
        return pages_no

    
    def extend_page_data(self, old, new):
        # 6 categories in dict: titles, countries, genres, dates, years, ratings
        old['titles'].extend(new['titles'])
        old['countries'].extend(new['countries'])
        old['genres'].extend(new['genres'])
        old['dates'].extend(new['dates'])
        old['years'].extend(new['years'])
        old['ratings'].extend(new['ratings'])
        return old

    def get_all_data(self, username):
        pages_no = self.calculate_number_of_pages(username)
        for i in range(1, pages_no + 1):
            page_data = self.get_all_page_data(username, i)
            if i == 1:
                data = page_data
            else:
                data = self.extend_page_data(data, page_data)
        return data

    def get_countries_from_page(self, page):
        soup = BeautifulSoup(page)
        divs = soup.find_all('div', class_='filmPreview__info filmPreview__info--countries')
        if divs is None:
            print('Parsing page failed.')
            return None
        countries = []
        for div in divs:
            ul = div.contents[1]
            movie_countries = []
            for li in ul.contents:
                movie_countries.append(li.get_text())
            countries.append(movie_countries)
        return countries

    #TODO Remove duplication
    def get_genres_from_page(self, page):
        soup = BeautifulSoup(page)
        divs = soup.find_all('div', class_='filmPreview__info filmPreview__info--genres')
        if divs is None:
            print('Parsing page failed.')
            return None
        genres = []
        for div in divs:
            ul = div.contents[1]
            movie_genres = []
            for li in ul.contents:
                movie_genres.append(li.get_text())
            genres.append(movie_genres)
        return genres

    def get_all_page_data(self, username, page_no):
        page_data = dict()
        page = self.get_ratings_page(username, page_no)
        page_data['titles'] = self.get_titles_from_page(page)
        page_data['countries'] = self.get_countries_from_page(page)
        page_data['genres'] = self.get_genres_from_page(page)
        page_data['ratings'] = self.get_ratings_from_page(page)
        page_data['dates'] = self.get_watch_dates_from_page(page) # TODO parse dates
        page_data['years'] = self.get_production_years_from_page(page)
        return page_data
