from bs4 import BeautifulSoup


def parse_film(soup):
    film_info = {}
    items_dark = soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')
    if items_dark:
        row = 'rowDark__2qC4I'
        value = 'valueDark__3dsUz'
        link = 'linkDark__3aytH'
        title = 'titleDark__3-gXe'
        root = 'rootInLight__3r1yx'
    else:
        row = 'rowLight__3uy9z'
        value = 'valueLight__3Gl7S'
        link = 'linkLight__1Nxon'
        title = 'titleLight__1AL-E'
        root = 'rootInDark__3mPn2'
    items = soup.find_all('div', class_=f'styles_{row} styles_row__2ee6F')
    film_name = soup.find('span', class_='styles_title__2l0HH').get_text()
    film_img = soup.find('img', class_=f'film-poster styles_root__2Q5Ds styles_{root} image styles_root__eMUmk styles_rootLoaded__SyGwc')
    film_img = film_img.attrs['src']
    film_description = soup.find('p', class_='styles_paragraph__2Otvx').get_text()
    worldwide_total = soup.find('div', class_=f'styles_{value} styles_value__2F1uj styles_root__RwScy')
    if worldwide_total:
        worldwide_total = worldwide_total.find('a', class_=f'styles_{link} styles_link__1N3S2')
        worldwide_total = worldwide_total.get_text().replace(u'\xa0', u' ')
        film_info['Сборы в мире'] = worldwide_total
    film_info['Название фильма'] = film_name
    film_info['Изображение'] = film_img
    film_info['Описание'] = film_description
    for item in items:
        item_1 = item.find('div', class_=f'styles_{title} styles_title__a0_0F')
        if item_1:
            if item_1.get_text() not in ['Возраст', 'Рейтинг MPAA','Премьера в Росcии', 'Сборы в мире']:
                film_info[item.find('div', class_=f'styles_{title} styles_title__a0_0F').get_text()] \
                    = item.find('div', class_=f'styles_{value} styles_value__2F1uj').get_text().replace(u'\xa0', u' ')
    return film_info
