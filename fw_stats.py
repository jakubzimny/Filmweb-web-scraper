#!/var/www/html/wsgi/flask/bin/python3
from flask import Flask, render_template, jsonify, request, redirect
from scrape import Scraper
from data_analysis import DatasetAnalyzer
import eventlet
import time
from multiprocessing.pool import ThreadPool
from itertools import repeat

eventlet.monkey_patch()

app = Flask(__name__)

@app.route("/")
def index():   
    return render_template('template.html')

def download_page(username, page_no):
    scraper = Scraper()
    scraper.login()
    page_data = scraper.get_all_page_data(username, page_no)
    return page_data

@app.route("/scrape", methods=['POST'])
def scrape():
    start = time.time()
    scraper = Scraper()
    t1 = time.time()
    print(str(t1-start) + "s Load" )
    scraper.login()
    t2 = time.time()
    print(str(t2-t1) + "s Login" )
    if request.is_json:
        username = request.get_json()['username']
    else:
        return 'Wystąpił problem podczas wysyłania danych.'
    pages_no = scraper.calculate_number_of_pages(username)
    t3 = time.time()
    print(str(t3-t2) + "s 1" )
    if pages_no is None:
        return 'Wystąpił błąd przy pobieraniu danych dla '+username\
            +'. Upewnij się, że masz FW_Stats w znajomych na Filmwebie.'
    # with ThreadPool(3) as pool:
    #     pool.starmap(download_page, repeat(username), zip(range(1,3)))
        
    #page_data = scraper.get_all_page_data(username, 1)
    page_data = scraper.get_all_data(username)
    t4 = time.time()
    print(str(t4-t3) + "s 2" )

    analyzer = DatasetAnalyzer(page_data)
    analyzer.plot_category('ratings', 'pie', 'Oceny')
    analyzer.plot_category('countries', 'bar', 'Kraje pochodzenia','#1a53af')
    analyzer.plot_category('genres', 'bar', 'Gatunki', '#48bc0f',)
    analyzer.plot_category('years', 'line', 'Lata produkcji', '#e85e14')

    return 'Pobrano to i tamto'

@app.route('/result')
def show_result():
    return render_template("result_template.html")