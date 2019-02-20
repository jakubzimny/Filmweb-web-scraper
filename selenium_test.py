from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get('https://filmweb.pl/login')
driver.find_element_by_class_name('fwBtn--gold').click()
driver.find_element_by_class_name('authButton--filmweb').click()
driver.find_element_by_name('j_username').send_keys('FW_Stats')
driver.find_element_by_name('j_password').send_keys('bestsiteinwww')

driver.find_element_by_class_name('materialForm__submit').click()

driver.get('https://www.filmweb.pl/user/Haemable/films?page=5')
print(driver.page_source)

with open("./fw.html", 'w') as f:
    f.write(driver.page_source)

driver.quit()