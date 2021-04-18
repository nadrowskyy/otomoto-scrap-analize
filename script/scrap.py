import requests, bs4, pickle, pandas
from datetime import datetime
import concurrent.futures
import time
headers = requests.utils.default_headers()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
global ITERATOR
ITERATOR = 0

lookup_table = {
    "stycznia": "01",   "lutego": "02",
    "marca": "03",       "kwietnia": "04",
    "maja": "05",           "czerwca": "06",
    "lipca": "07",       "sierpnia": "08",
    "września": "09",  "października": "10",
    "listopada": "11", "grudnia": "12"
}


# GLOBAL DATA FRAME FOR ALL AUCTIONS
DATA_FRAME = pandas.DataFrame(columns=['ID', 'Marka', 'Model', 'Miasto', 'Wojewodztwo','Moc', 'Poj. sil', 'Cena',
                                       'Waluta','Kraj poch.', 'Czy zabytek', 'Czy zarej. w Polsce', 'Czy bezwypadkowy',
                                       'Czy Anglik','Serwisowany w ASO', 'Filtr DPF', 'Generacja',
                                       'Rok prod.', 'Pierwsza rejestracja','Przebieg', 'Oferta od', 'Czy leasing',
                                       'Rodzaj paliwa', 'Emisja CO2', 'Typ', 'Kolor', 'Stan', 'Czy pierwsz. właśc',
                                       'Napęd', 'Skrzynia biegów', 'Data dodania', 'Link'])



# SCRAPPING DATA FROM FOR EACH AUCTION
def scrap_data_for_offer(b, m, url, loc):
    page = requests.get(url, headers=headers)
    data = page.text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    brand = b
    model = m
    city = loc[0].strip()
    # print(city)
    region = loc[1].strip('()')
    # print(region)

    id_offer = None
    if soup.find_all('span', {'id':'ad_id'}):
        try:
            id_offer = str(soup.find_all('span', {'id':'ad_id'})[0].text)
        except:
            pass
    print('ID', id_offer)

    power = None
    if soup.find_all('span', string='Moc'):
        try:
            power = int(soup.find_all('span', string='Moc')[0].parent.contents[3].text.strip().split(' ')[0])
        except:
            pass
    # print('Moc', power)

    eng_cap = None
    if soup.find_all('span', string='Pojemność skokowa'):
        try:
            eng_cap = soup.find_all('span', string='Pojemność skokowa')[0].parent.contents[3].text.strip().split(' ')[:-1]
            eng_cap = int(''.join(eng_cap))
        except:
            pass
    # print('Poj. sil.', eng_cap)

    price = None
    if soup.find_all('span', {'class':'offer-price__number'}):
        try:
            price = soup.find_all('span', {'class':'offer-price__number'})[1].text.strip().split(' ')[:-1]
            price = int(''.join(price))
        except:
            pass
    # print('Cena', price)

    currency = None
    if soup.find_all('span', {'class': 'offer-price__currency'}):
        try:
            currency = soup.find_all('span', {'class': 'offer-price__currency'})[1].text

        except:
            pass
    # print('Waluta', currency)

    from_country = None
    if soup.find_all('span', string='Kraj pochodzenia'):
        try:
            from_country = soup.find_all('span', string='Kraj pochodzenia')[0].parent.contents[3].find('a').text.strip()
        except:
            pass
    # print('Kraj pochodzenia', from_country)

    if_vintage = False
    if soup.find_all('span', string='Zarejestrowany jako zabytek'):
        try:
            if_vintage = soup.find_all('span', string='Zarejestrowany jako zabytek')[0].parent.contents[3].find('a')\
                .text.strip()
            if_vintage = True if if_vintage == 'Tak' else if_vintage
            if_vintage = False if if_vintage == 'Nie' else if_vintage
        except:
            pass
    # print('Czy zabytek', if_vintage)

    if_reg_in_poland = None
    if soup.find_all('span', string='Zarejestrowany w Polsce'):
        try:
            if_reg_in_poland = soup.find_all('span', string='Zarejestrowany w Polsce')[0].parent.contents[3].find('a') \
                .text.strip()
            if_reg_in_poland = True if if_reg_in_poland == 'Tak' else False
            if_reg_in_poland = False if if_reg_in_poland == 'Nie' else False
        except:
            pass
    # print('Czy zar w polsce', if_reg_in_poland)

    if_acc_free = None
    if soup.find_all('span', string='Bezwypadkowy'):
        try:
            if_acc_free = soup.find_all('span', string='Bezwypadkowy')[0].parent.contents[3].find(
                'a').text.strip()
            if_acc_free = True if if_acc_free == 'Tak' else if_acc_free
            if_acc_free = False if if_acc_free == 'Nie' else if_acc_free
        except:
            pass
    # print('Bezwypadkowy', if_acc_free)

    if_right_wheel = None
    if soup.find_all('span', string='Kierownica po prawej (Anglik)'):
        try:
            if_right_wheel = soup.find_all('span', string='Kierownica po prawej (Anglik)')[0].parent.contents[3].find(
                'a').text.strip()
            if_right_wheel = True if if_right_wheel == 'Tak' else if_right_wheel
            if_right_wheel = False if if_right_wheel == 'Nie' else if_right_wheel
        except:
            pass
    # print('Czy anglik', if_right_wheel)

    if_aso = None
    if soup.find_all('span', string='Serwisowany w ASO'):
        try:
            if_aso = soup.find_all('span', string='Serwisowany w ASO')[0].parent.contents[3].find(
                'a').text.strip()
            if_aso = True if if_aso == 'Tak' else if_aso
            if_aso = False if if_aso == 'Nie' else if_aso
        except:
            pass
    # print('Serwisowany w ASO', if_aso)


    # NIE DZIALA DLA KAZDEGO OGLOSZENIA
    # if_vat = None
    # if soup.find_all('span', string='Faktura VAT'):
    #     if_vat = soup.find_all('span', string='Faktura VAT')[0].parent.contents[3].find(
    #         'a').text.strip()
    #     if_vat = True if if_vat == 'Tak' else if_vat
    #     if_vat = False if if_vat == 'Nie' else if_vat
    # print('Czy faktura VAT', if_vat)

    if_dpf = None
    if soup.find_all('span', string='Filtr cząstek stałych'):
        try:
            if_dpf = soup.find_all('span', string='Filtr cząstek stałych')[0].parent.contents[3].find(
                'a').text.strip()
            if_dpf = True if if_dpf == 'Tak' else if_dpf
            if_dpf = False if if_dpf == 'Nie' else if_dpf
        except:
            pass
    # print('Filtr cząstek stałych', if_dpf)

    generation = None
    if soup.find_all('span', string='Generacja'):
        try:
            generation = soup.find_all('span', string='Generacja')[0].parent.contents[3].find(
                'a').text.strip()
        except:
            pass
    # print('Generacja', generation)

    prod_year = None
    if soup.find_all('span', string='Rok produkcji'):
        try:
            prod_year = int(soup.find_all('span', string='Rok produkcji')[0].parent.contents[3].text.strip())
        except:
            pass
    # print('Rok produkcji', prod_year)

    first_register = None
    if soup.find_all('span', string='Pierwsza rejestracja'):
        try:
            first_register = soup.find_all('span', string='Pierwsza rejestracja')[0].parent.contents[3].text.strip()
            first_register = datetime.strptime(first_register, '%d/%m/%Y')
        except:
            pass
    # print('Pierwsza rejestracja', first_register)

    mileage = None
    if soup.find_all('span', string='Przebieg'):
        try:
            mileage = soup.find_all('span', string='Przebieg')[0].parent.contents[3].text.strip().split(' ')[:-1]
            mileage = int(''.join(mileage))
        except:
            pass
    # print('Przebieg', mileage)

    offer_from = None
    if soup.find_all('span', string='Oferta od'):
        try:
            offer_from = soup.find_all('span', string='Oferta od')[0].parent.contents[3].find(
                'a').text.strip()
        except:
            pass
    # print('Oferta od', offer_from)

    if_leasing = None
    if soup.find_all('span', string='Leasing'):
        try:
            if_leasing = soup.find_all('span', string='Leasing')[0].parent.contents[3].find('a').text.strip()
            if_leasing = True if if_leasing == 'Tak' else if_leasing
            if_leasing = False if if_leasing == 'Nie' else if_leasing
        except:
            pass
    # print('leasing', if_leasing)

    fuel_type = None
    if soup.find_all('span', string='Rodzaj paliwa'):
        try:
            fuel_type = soup.find_all('span', string='Rodzaj paliwa')[0].parent.contents[3].find(
                'a').text.strip()
        except:
            pass
    # print('Rodzaj paliwa', fuel_type)

    co2_emission = None
    if soup.find_all('span', string='Emisja CO2'):
        try:
            co2_emission = soup.find_all('span', string='Emisja CO2')[0].parent.contents[3].text.strip().split(' ')[:-1]
            co2_emission = int(''.join(co2_emission))
        except:
            pass
    # print('Emisja CO2 [g/kg]', co2_emission)

    car_type = None
    if soup.find_all('span', string='Typ'):
        try:
            car_type = soup.find_all('span', string='Typ')[0].parent.contents[3].find(
                'a').text.strip()
        except:
            pass
    # print('Typ', car_type)

    color = None
    if soup.find_all('span', string='Kolor'):
        try:
            color = soup.find_all('span', string='Kolor')[0].parent.contents[3].find(
                'a').text.strip()
        except:
            pass
    # print('Kolor', color)

    condition = None
    if soup.find_all('span', string='Stan'):
        try:
            condition = soup.find_all('span', string='Stan')[0].parent.contents[3].find(
                'a').text.strip()
        except:
            pass
    # print('Stan', condition)

    if_first_owner = None
    if soup.find_all('span', string='Pierwszy właściciel'):
        try:
            if_first_owner = soup.find_all('span', string='Pierwszy właściciel')[0].parent.contents[3].find(
                'a').text.strip()
            if_first_owner = True if if_first_owner == 'Tak' else if_first_owner
            if_first_owner = False if if_first_owner == 'Nie' else if_first_owner
        except:
            pass
    # print('Pierwszy właściciel', if_first_owner)

    drive = None
    if soup.find_all('span', string='Napęd'):
        try:
            drive= soup.find_all('span', string='Napęd')[0].parent.contents[3].find(
                'a').text.strip()
        except:
            pass
    # print('Napęd', drive)

    transmission_type = None
    if soup.find_all('span', string='Skrzynia biegów'):
        try:
            transmission_type = soup.find_all('span', string='Skrzynia biegów')[0].parent.contents[3].find(
                'a').text.strip()
        except:
            pass
    # print('Skrzynia biegów', transmission_type)

    date = None
    if soup.find_all('span', {'class': 'offer-meta__value'}):
        try:
            date = soup.find_all('span', {'class': 'offer-meta__value'})[0].string
            date = date.split(' ')
            tmp_month = ''
            for k, v in lookup_table.items():
                tmp_month = date[2]
                if k == tmp_month:
                    tmp_month = v
                    break
            date[2] = tmp_month
            date = ' '.join(date)
            #print(date)
            date = datetime.strptime(date, '%H:%M, %d %m %Y')
        except:
            pass
    #print(date)

    # print('Data dodania', date)
    tmp_data_frame = pandas.DataFrame(
        [(id_offer, brand, model, city, region, power, eng_cap, price, currency,from_country, if_vintage,
          if_reg_in_poland, if_acc_free, if_right_wheel, if_aso, if_dpf, generation, prod_year, first_register, mileage,
          offer_from, if_leasing, fuel_type, co2_emission, car_type, color,
          condition, if_first_owner, drive, transmission_type, date, url)],
        columns=['ID', 'Marka', 'Model', 'Miasto', 'Wojewodztwo','Moc', 'Poj. sil', 'Cena', 'Waluta','Kraj poch.',
                 'Czy zabytek', 'Czy zarej. w Polsce', 'Czy bezwypadkowy', 'Czy Anglik','Serwisowany w ASO',
                'Filtr DPF', 'Generacja', 'Rok prod.', 'Pierwsza rejestracja','Przebieg', 'Oferta od', 'Czy leasing',
                'Rodzaj paliwa', 'Emisja CO2', 'Typ', 'Kolor', 'Stan',
                'Czy pierwsz. właśc', 'Napęd', 'Skrzynia biegów', 'Data dodania', 'Link']
        )
    global ITERATOR
    ITERATOR+=1
    if ITERATOR == 1:
        tmp_data_frame.to_csv(f'cars/{brand}.csv', index=False)
    else:
        tmp_data_frame.to_csv(f'cars/{brand}.csv', mode='a', index=False, header=False)
    print(ITERATOR, 'elementow')


# GETTING LINK TO AUCTION FOR EACH MODEL
def get_link_from_page(cars_dict):
    car_url = 'https://www.otomoto.pl/osobowe'
    for brand, models in cars_dict.items():
        print(brand)
        for model in models:
            print(model)
            tmp_url = f'{car_url}/{brand}/{model}/'
            page = requests.get(tmp_url, headers=headers)
            data = page.text
            soup = bs4.BeautifulSoup(data, 'html.parser')
            if soup.find_all('span', class_='page'):
                num_pages = int(soup.find_all('span', class_='page')[-1].string)
            else:
                num_pages = 1
            for i in range(1, num_pages+1):
                cars_page = requests.get(f'{tmp_url}?page={i}')
                cars_data = cars_page.text
                cars_soup = bs4.BeautifulSoup(cars_data, 'html.parser')
                # LINKI DO AUKCJI
                cars_links = cars_soup.find_all('a', class_='offer-title__link')
                cars_cities = cars_soup.find_all('span', class_='ds-location-city')
                cars_regions = cars_soup.find_all('span', class_='ds-location-region')
                cars_link_dict = {}
                for link, city, region in zip(cars_links, cars_cities, cars_regions):
                    cars_link_dict[link.get('href')] = [city.string, region.string]

                for link, location in cars_link_dict.items():
                    # CALL A FUNCTION FOR EACH AUCTION TO SCRAP NEEDED DATA FROM THERE
                    time.sleep(1)
                    scrap_data_for_offer(brand, model, link, location)
    global ITERATOR
    ITERATOR = 0


if __name__ == '__main__':
    get_link_from_page(cars_dict)
