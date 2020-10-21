import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import csv
from film_parse import parse_film

HOST = 'https://www.kinopoisk.ru'
URL = 'https://www.kinopoisk.ru/lists/top250/?page=1&tab=all'
HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
           'cache-control': 'max-age=0',
           'cookie': 'mda_exp_enabled=1; _ym_uid=158308485055319303; mda=0; yandexuid=4901252881583052573;'
                     ' yuidss=4901252881583052573; gdpr=0; my_perpages=%5B%5D; lfiltr=all;'
                     ' yandex_login=dzougov91; i=Zz0/JxcfNs0FyhgOwOhIee7/Zop+AwddEzR/y7Pz4ZcbDem6oGGFPoJb9'
                     'O2cw14AEXxZn4rtCaQxFabz9CTMbcOjNdg=; location=1; crookie=3vzDBBKvhmKeMP2l67ougYclXnMhy4'
                     'ElHNplxICsX6MWOYBQMGe9V3SXAKSCuuzLJFq89w0l8orP3Em3RXdP0xBPECo=; cmtchd=MTYwMzEwNTE1MjQ1Mw'
                     '==; tc=1; mobile=no; yandex_ugc_rating_status=no; yandex_ugc_rating_status.sig=pw4cVz6AAY2ip'
                     'ArQXugmwejk7uw; user-geo-region-id=114769; user-geo-country-id=2; desktop_session_key=3bedef752'
                     'c1fda9332129cf85721fc706c4286c0ff924eb147f0765ee68f7f3f1f9b6b5ef7a6860859a9408ff2dff27e72668d6b7'
                     'e09e02cc74bdff8ab87fd34907e84cc98f7a18ab2f142276287655a2f6b21aaba612ab81e28219f0d3e4d04; desktop_'
                     'session_key.sig=42M-mmA9h9j-z-egWOypDwXxH2A; _ym_isad=1; _csrf=w6zRgkZASFpsGgBUp9p33Qnd; PHPSESSID'
                     '=m6svphph3hu5r6ii4li00j9kr2; yandex_gid=213; uid=21827928; user_country=ru; _ym_wasSynced=%7B%22tim'
                     'e%22%3A1603203638113%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; _ym_visorc_56'
                     '177992=w; _ym_visorc_26812653=b; yp=1603290037.yu.4901252881583052573; ymex=1605795637.oyu.490125288158'
                     '3052573; _ym_visorc_237742=w; _ym_visorc_22663942=w; ya_sess_id=3:1603203636.5.0.1598545482651:-kj8bQ:29.'
                     '1|111141043.0.2|30:193363.197842.fTxh9ZkLWpBD4sjyoruTHG0zDH0; ys=udn.cDpkem91Z292OTE%3D#c_chck.1791289350; '
                     'mda2_beacon=1603203636902; sso_status=sso.passport.yandex.ru:synchronized; _ym_visorc_238724=w; kdetect=1; _'
                     'csrf_csrf_token=OpPdtYMCN02nuGUgp4hYoQJIO33ZdcQsEOSqQTTwJ5U; _ym_visorc_238735=w; _ym_d=1603205893; kpunk=1',
           'dnt': '1',
           'sec-fetch-dest': 'document',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'same-origin',
           'sec-fetch-user': '?1',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/86.0.4240.75 Safari/537.36', }


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html, films_url):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='selection-film-item-meta__link')
    for item in items:
        films_url.append(HOST + item.attrs['href'])
    return films_url


def parse_films_url():
    films_url = []
    for i in range(4):
        url = f'https://www.kinopoisk.ru/lists/top250/?page={i + 1}&tab=all'
        html = get_html(url)
        if html.status_code == 200:
            get_content(html.text, films_url)
        else:
            print('Error')
    return films_url


def get_film_content():
    films_url = parse_films_url()
    top120_films = {}
    for index, film_url in enumerate(films_url):
        html = get_html(film_url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            top120_films[index + 1] = parse_film(soup)
        else:
            print('Error')
    with open('films.txt', 'w') as outfile:
        json.dump(top120_films, outfile)


get_film_content()
