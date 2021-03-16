import requests, bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle

# PATH TO CHROMEDRIVER, NEEDED TO RUN SELENIUM. IMPORTANT! -VERSION OF CHROMEDRIVER HAVE TO EQUAL TO VERSION OF OUR
# CHROME BROWSER- https://chromedriver.chromium.org/downloads
CHROMEDRIVER_PATH = 'C:/Users/Ja/Desktop/kursy kursiki/vi semestr/P Przetwarzanie dużych zbiorów informacji/chromedriver.exe'

def get_cars_brand(url):
    # TO GET BRANDS OF CARS WE USE REQUESTS LIBRARY, USING THIS LIBRARY WE CAN DOWNLOAD THE PAGE
    # AND THEN SCRAP INFO FROM IT USING BEAUTIFULSOUP
    page = requests.get(url)
    data = page.text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    cars = soup.find('select', title='Marka pojazdu').find_all('option')
    # SCRAPPED BRANDS ARE SAVED TO cars_dict DICTIONARY
    cars_dict = dict()
    for car in cars[1:]:
        if car['value'] == 'warszawa':
            cars_dict['marka_warszawa'] = ''
        else:
            cars_dict[car['value']] = ''
    print(cars_dict)
    return cars_dict

def get_cars_model(cars_dict):
    # TO GET MODELS OF EACH BRAND WE NEED TO USE SELENIUM FRAMEWORK(BEACAUSE MODELS ON SITE ARE LOADED DYNAMICALYY BY
    # JS SCRIPT). THIS FRAMEWORK USUALLY OPEN NEW BROWSER WINDOW, GOES TO PAGE AND THEN SCRAP DATA, BUT WE CAN RUN
    # IT IN 'NO WINDOW' MODE
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

    for brand, model in cars_dict.items():
        path = 'https://www.otomoto.pl/osobowe/' + brand
        driver.get(path)
        select = driver.find_element_by_xpath("//select[@id='param573']")
        splitted_list = select.text.splitlines()
        car_names = []
        for el in splitted_list[1:]:
            el = el.split(' ')[:-1]
            car = '-'.join(el).lower().replace('(', '').replace(')', '')
            if car == 'inny':
                car = 'other'
            car_names.append(car)
        # FOR EACH BRAND WE HAVE A LIST OF MODELS IN DICTIONARY
        cars_dict[brand] = car_names
        print(cars_dict)
    # DATA IS DUMPED TO A PICKLE TO WE CAN USE IT LATER
    pickle_out = open('dict_cars.pickle', 'wb')
    pickle.dump(cars_dict, pickle_out)
    pickle_out.close()

    driver.quit()

url = 'https://www.otomoto.pl/osobowe/acura/'
cars_dict = get_cars_brand(url)
get_cars_model(cars_dict)