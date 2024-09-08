import requests
from bs4 import BeautifulSoup

def parse_weather(link):
    data = {}
    with requests.Session() as session:
        responce = session.get(link)
        soupe = BeautifulSoup(responce.text, 'lxml')
        for i in range(1,8):
            d = soupe.find('div', id = f'bd{i}').text
            data[i] = d.split()
    return data
