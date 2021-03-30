import requests, bs4, pickle, pandas

# GLOBAL DATA FRAME FOR ALL AUCTIONS
DATA_FRAME = pandas.DataFrame(columns=['ID', 'Marka', 'Model', 'Moc', 'Poj. sil', 'Cena', 'Kraj poch.',
                                        'Miasto', 'Wojewwdztwo','Czy zabytek', 'Czy bezwypadkowy', 'Serwisowany w ASO',
                                        'Filtr DPF', 'Generacja', 'Rok prod.', 'Przebieg', 'Oferta od',
                                        'Rodzaj paliwa', 'Emisja CO2', 'Typ', 'Kolor', 'Stan',
                                        'Czy pierwsz. właśc', 'Napęd', 'Skrzynia biegów', 'Data dodania'])


# SCRAPPING DATA FROM FOR EACH AUCTION
def scrap_data_for_offer(b, m, url, loc):
    page = requests.get(url)
    data = page.text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    brand = b
    model = m
    city = loc[0].strip()
    region = loc[1].strip('()')

    id_offer = None
    if soup.find_all('span', {'id':'ad_id'}):
        id_offer = soup.find_all('span', {'id':'ad_id'})[0].text
    print('ID', id_offer)

    power = None
    if soup.find_all('span', string='Moc'):
        power = soup.find_all('span', string='Moc')[0].parent.contents[3].text.strip()
    # print('Moc', power)

    eng_cap = None
    if soup.find_all('span', string='Pojemność skokowa'):
        eng_cap = soup.find_all('span', string='Pojemność skokowa')[0].parent.contents[3].text.strip()
    # print('Poj. sil.', eng_cap)

    price = None
    if soup.find_all('span', {'class':'offer-price__number'}):
        price = soup.find_all('span', {'class':'offer-price__number'})[1].text.strip()
    # print('Cena', price)

    # NIE WE WSZYSTKICH OGŁOSZENIACH PODANE SĄ WOJEWÓDZTWA, POTRZEBNA BĘDZIE FUNKCJA DOPASOWUJĄCA MIASTO
    # DO WOJEWÓDZTWA ALBO TO OLEJEMY
    #city = soup.find_all('span', {'class':'seller-box__seller-address__label'})[0].text.strip().split(',')
    #print(city)


    from_country = None
    if soup.find_all('span', string='Kraj pochodzenia'):
        from_country = soup.find_all('span', string='Kraj pochodzenia')[0].parent.contents[3].find('a').text.strip()
    # print('Kraj pochodzenia', from_country)

    if_vintage = None
    if soup.find_all('span', string='Zarejestrowany jako zabytek'):
        if_vintage = soup.find_all('span', string='Zarejestrowany jako zabytek')[0].parent.contents[3].find('a').text.strip()
    # print('Czy zabytek', if_vintage)

    if_acc_free = None
    if soup.find_all('span', string='Bezwypadkowy'):
        if_acc_free = soup.find_all('span', string='Bezwypadkowy')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Bezwypadkowy', if_acc_free)

    if_aso = None
    if soup.find_all('span', string='Serwisowany w ASO'):
        if_aso = soup.find_all('span', string='Serwisowany w ASO')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Serwisowany w ASO', if_aso)

    if_dpf = None
    if soup.find_all('span', string='Filtr cząstek stałych'):
        if_dpf = soup.find_all('span', string='Filtr cząstek stałych')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Filtr cząstek stałych', if_dpf)

    generation = None
    if soup.find_all('span', string='Generacja'):
        generation = soup.find_all('span', string='Generacja')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Generacja', generation)

    prod_year = None
    if soup.find_all('span', string='Rok produkcji'):
        prod_year = soup.find_all('span', string='Rok produkcji')[0].parent.contents[3].text.strip()
    # print('Rok produkcji', prod_year)

    mileage = None
    if soup.find_all('span', string='Przebieg'):
        mileage = soup.find_all('span', string='Przebieg')[0].parent.contents[3].text.strip()
    # print('Przebieg', mileage)

    offer_from = None
    if soup.find_all('span', string='Oferta od'):
        offer_from = soup.find_all('span', string='Oferta od')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Oferta od', offer_from)

    fuel_type = None
    if soup.find_all('span', string='Rodzaj paliwa'):
        fuel_type = soup.find_all('span', string='Rodzaj paliwa')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Rodzaj paliwa', fuel_type)

    co2_emission = None
    if soup.find_all('span', string='Emisja CO2'):
        co2_emission = soup.find_all('span', string='Emisja CO2')[0].parent.contents[3].text.strip()
    # print('Emisja CO2', co2_emission)

    car_type = None
    if soup.find_all('span', string='Typ'):
        car_type = soup.find_all('span', string='Typ')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Typ', car_type)

    color = None
    if soup.find_all('span', string='Kolor'):
        color = soup.find_all('span', string='Kolor')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Kolor', color)

    condition = None
    if soup.find_all('span', string='Stan'):
        condition = soup.find_all('span', string='Stan')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Stan', condition)

    if_first_owner = None
    if soup.find_all('span', string='Pierwszy właściciel'):
        if_first_owner = soup.find_all('span', string='Pierwszy właściciel')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Pierwszy właściciel', if_first_owner)

    drive = None
    if soup.find_all('span', string='Napęd'):
        drive= soup.find_all('span', string='Napęd')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Napęd', drive)

    transmission_type = None
    if soup.find_all('span', string='Skrzynia biegów'):
        transmission_type = soup.find_all('span', string='Skrzynia biegów')[0].parent.contents[3].find(
            'a').text.strip()
    # print('Skrzynia biegów', transmission_type)

    date = None
    if soup.find_all('span', {'class': 'offer-meta__value'})[0]:
        date = soup.find_all('span', {'class': 'offer-meta__value'})[0].string
    # print('Data dodania', date)
    tmp_data_frame = pandas.DataFrame(
        [(id_offer, brand, model, power, eng_cap, price, from_country, city, region, if_vintage, if_acc_free, if_aso,
          if_dpf, generation, prod_year, mileage, offer_from, fuel_type, co2_emission, car_type, color,
          condition, if_first_owner, drive, transmission_type, date)],
        columns=['ID', 'Marka', 'Model', 'Moc', 'Poj. sil', 'Cena', 'Kraj poch.',
                'Miasto', 'Wojewwdztwo', 'Czy zabytek', 'Czy bezwypadkowy', 'Serwisowany w ASO',
                'Filtr DPF', 'Generacja', 'Rok prod.', 'Przebieg', 'Oferta od',
                'Rodzaj paliwa', 'Emisja CO2', 'Typ', 'Kolor', 'Stan',
                'Czy pierwsz. właśc', 'Napęd', 'Skrzynia biegów', 'Data dodania']
        )
    #print(tmp_data_frame)
    global DATA_FRAME
    DATA_FRAME = DATA_FRAME.append(tmp_data_frame, ignore_index=True)
    # print(DATA_FRAME)
    print(DATA_FRAME.to_string())
    # print('\n')


# GETTING LINK TO AUCTION FOR EACH MODEL
def get_link_from_page(car_url, cars_dict):
    # auction_links = []

    for brand, models in cars_dict.items():
        for model in models:
            print(model)
            tmp_url = f'{car_url}/{brand}/{model}/'
            #print(tmp_url)
            #print(tmp_url)
            page = requests.get(tmp_url)
            data = page.text
            soup = bs4.BeautifulSoup(data, 'html.parser')
            if soup.find_all('span', class_='page'):
                num_pages = int(soup.find_all('span', class_='page')[-1].string)
            else:
                num_pages = 1
            for i in range(1, num_pages+1):
                cars_page = requests.get(f'{tmp_url}?page={i}')
                #print(cars_page)
                cars_data = cars_page.text
                cars_soup = bs4.BeautifulSoup(cars_data, 'html.parser')
                # LINKI DO AUKCJI
                cars_links = cars_soup.find_all('a', class_='offer-title__link')
                cars_cities = cars_soup.find_all('span', class_='ds-location-city')
                cars_regions = cars_soup.find_all('span', class_='ds-location-region')
                print(len(cars_links))
                print(len(cars_cities))
                print(len(cars_regions))

                cars_link_dict = {}
                for link, city, region in zip(cars_links, cars_cities, cars_regions):
                    cars_link_dict[link.get('href')] = [city.string, region.string]

                for link, location in cars_link_dict.items():
                    # CALL A FUNCTION FOR EACH AUCTION TO SCRAP NEEDED DATA FROM THERE
                    scrap_data_for_offer(brand, model, link, location)
            


pickle_in = open('dict_cars.pickle', 'rb')
cars_dict = pickle.load(pickle_in)
pickle_in.close()
url = 'https://www.otomoto.pl/osobowe'
get_link_from_page(url, cars_dict)
