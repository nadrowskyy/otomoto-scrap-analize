import requests, bs4, pickle

# SCRAPPING DATA FROM FOR EACH AUCTION
def scrap_data_for_offer(url):
    page = requests.get(url)
    data = page.text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    id_offer = None
    if soup.find_all('span', {'id':'ad_id'}):
        id_offer = soup.find_all('span', {'id':'ad_id'})[0].text
    print('id', id_offer)
    power = None
    if soup.find_all('span', string='Moc'):
        power = soup.find_all('span', string='Moc')[0].parent.contents[3].text.strip()
    print('moc', power)
    eng_cap = None
    if soup.find_all('span', string='Pojemność skokowa'):
        eng_cap = soup.find_all('span', string='Pojemność skokowa')[0].parent.contents[3].text.strip()
    print('poj. sil', eng_cap)
    price = None
    if soup.find_all('span', {'class':'offer-price__number'}):
        price = soup.find_all('span', {'class':'offer-price__number'})[1].text.strip()
    print('cena', price)
    # ZA DUZO LOSOWYCH DANYCH
    # city = soup.find_all('span', {'class':'seller-box__seller-address__label'})[0].text.strip().split(',')[0]
    # print(city)
    from_country = None
    if soup.find_all('span', string='Kraj pochodzenia'):
        from_country = soup.find_all('span', string='Kraj pochodzenia')[0].parent.contents[3].find('a').text.strip()
    print('kraj pochodzenia', from_country)
    # TUTAJ BEDZIE RESZTA PARAMETROW DO ZESRAPOWANIA


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
                for link in cars_links:
                    #print(link.get('href'))
                    # CALL A FUNCTION FOR EACH AUCTION TO SCRAP NEEDED DATA FROM THERE
                    scrap_data_for_offer(link.get('href'))
                    #print(link.get('href'))
                    #auction_links.append(link.get('href'))
            #print(len(auction_links))

pickle_in = open('dict_cars.pickle', 'rb')
cars_dict = pickle.load(pickle_in)
pickle_in.close()
url = 'https://www.otomoto.pl/osobowe'
get_link_from_page(url, cars_dict)

