import requests, bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle

# PATH TO CHROMEDRIVER, NEEDED TO RUN SELENIUM. IMPORTANT! -VERSION OF CHROMEDRIVER HAVE TO BE EQUAL TO VERSION OF OUR
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
            continue
        if car['value'] == 'radical':
            continue
        if car['value'] == 'other':
            continue
        else:
            cars_dict[car['value']] = ''
    print(cars_dict)
    return cars_dict

def get_cars_model(cars_dict):
    # TO GET MODELS OF EACH BRAND WE NEED TO USE SELENIUM FRAMEWORK(BEACAUSE MODELS ON SITE ARE LOADED DYNAMICALLY BY
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
        print('------------MARKA', brand)
        for el in splitted_list[1:]:
            print(el)
            el = el.split(' ')[:-1]
            car = '-'.join(el).lower().replace('(', '').replace(')', '')

            # SUPPORT FOR NON-TYPICAL MODELS NAME'S
            if car == 'inny':
                car = 'other'
            car = car.replace('.', '')

            if brand == 'ford':
                if car == 'ka+':
                    car = 'ka_plus'

            if brand == 'chrysler':
                if car == 'town-&-country':
                    car = 'town-country'

            if brand == 'kia':
                if car == "pro_cee'd":
                    car = 'pro-ceed'

            if brand == 'oldsmobile':
                if car == 'eighty---eight':
                    car = 'eighty-eight'

            if brand == 'suzuki':
                if car == 'wagon-r+':
                    car = 'wagon-r-'

            if brand == 'toyota':
                if car == 'prius+':
                    car = 'prius_plus'

            if brand == 'volkswagen':
                if car == 'up!':
                    car = 'up'

            if brand == 'mercedes-benz':
                if car == 'klasa-a':
                    car = 'a-klasa'
                if car == 'klasa-b':
                    car = 'b-klasa'
                if car == 'klasa-c':
                    car = 'c-klasa'
                if car == 'klasa-e':
                    car = 'e-klasa'
                if car == 'klasa-g':
                    car = 'g-klasa'
                if car == 'klasa-r':
                    car = 'r-klasa'
                if car == 'klasa-s':
                    car = 's-klasa'
                if car == 'klasa-v':
                    car = 'v-klasa'
                if car == 'klasa-x':
                    car = 'x-klasa'
                if car == 'cl':
                    car = 'cl-klasa'
                if car == 'cla':
                    car = 'cla-klasa'
                if car == 'clk':
                    car = 'clk-klasa'
                if car == 'cls':
                    car = 'cls-klasa'
                if car == 'gl':
                    car = 'gl-klasa'
                if car == 'gla':
                    car = 'gla-klasa'
                if car == 'glb':
                    car = 'glb-klasa'
                if car == 'glc':
                    car = 'glc-klasa'
                if car == 'gle':
                    car = 'gle-klasa'
                if car == 'glk':
                    car = 'glk-klasa'
                if car == 'gls':
                    car = 'gls-klasa'
                if car == 'ml':
                    car = 'm-klasa'
                if car == 'slk':
                    car = 'slk-klasa'
                if car == 'w201':
                    car = 'w201-190'

            if brand == 'nissan':
                if car == 'qashqai+2':
                    car = 'qashqai-2'

            if brand == 'citroen':
                if car == 'c-elysée':
                    car = 'c-elysee'

            car_names.append(car)
        # FOR EACH BRAND WE HAVE A LIST OF MODELS IN DICTIONARY
        cars_dict[brand] = car_names
        print(cars_dict)
    # DATA IS DUMPED TO A PICKLE SO WE CAN USE IT LATER
    pickle_out = open('dict_cars.pickle', 'wb')
    pickle.dump(cars_dict, pickle_out)
    pickle_out.close()

    driver.quit()

url = 'https://www.otomoto.pl/osobowe/acura/'
cars_dict = get_cars_brand(url)
get_cars_model(cars_dict)
