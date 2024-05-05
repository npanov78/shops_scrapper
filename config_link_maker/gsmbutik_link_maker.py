import logging
import requests
from bs4 import BeautifulSoup

from config.config import project_path
from config_link_maker.links import  gsmbutik_links


def configure_gsmbutik():
    logging.info(f'Начинаю собирать ссылки для gsmbutik.ru')
    for link in gsmbutik_links:
        response = requests.get(link)

        if response.status_code != 200:
            logging.error(f'Ошибка запроса для gsmbutik.ru: {link}; пропускаю...')
            continue
        soup = BeautifulSoup(response.text, 'html.parser')

        for product_elem in soup.find_all('div', class_='catalog-list__name'):
            a_tag = product_elem.find('a')
            if a_tag:
                product_link = a_tag.get('href')
                product_name = a_tag.text.strip()
                if product_name == '':
                    continue
                file_name = f"{project_path}/config/gsmbutik-urls.txt"
                full_link = f'{product_link}'

                with open(file_name, 'r') as file:
                    content = file.read()
                    if full_link in content:
                        continue
                    else:
                        with open(file_name, 'a') as file_a:
                            file_a.write(f"\n{full_link}")

    logging.info(f'Ссылки для gsmbutik.ru собраны')
