import requests
from bs4 import BeautifulSoup

def parse_link(city):
    err = False
    full_city = city.split(',')
    full_city.reverse()
    base_url = "https://ua.sinoptik.ua/%D1%83%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0" # for ukraine
    with requests.Session() as session:
        try:
            responce = session.get(base_url)
            soup = BeautifulSoup(responce.text, 'lxml')
            obl_find = soup.find('div', class_ = 'mapRightCol').find_all('a')
            for f_obl in obl_find:
                if full_city[1] in f_obl.text:
                    resp = session.get(f'https:{f_obl['href']}')
                    soupe = BeautifulSoup(resp.text, 'lxml')
                    reg_find = soupe.find('div', class_ = 'mapRightCol').find_all('a')
                    for f_reg in reg_find:
                        if full_city[2] in f_reg.text:
                            respon = session.get(f'https:{f_reg['href']}')
                            sou = BeautifulSoup(respon.text, 'lxml')
                            city_find = sou.find('div', class_='mapBotCol').find('div', class_='clearfix').find_all('a')
                            for f_city in city_find:
                                if full_city[3] in f_city.text:
                                    yield f'Data: https:{f_city['href']}'
                            else:
                                yield 'NoFind: населений пункт не знайдено'
                    else:
                        yield 'NoFind: Район не знайдено'
            else:
                yield 'NoFind: Область не знайдено'
        except Exception as R:
            yield R