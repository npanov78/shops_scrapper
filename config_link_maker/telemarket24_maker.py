import logging
import requests
from bs4 import BeautifulSoup
import http.client
http.client._MAXHEADERS = 1000
from config.config import project_path
from config_link_maker.links import telemarket24_links


def configure_telemarket24():
    logging.info(f'Начинаю собирать ссылки для telemarket24.ru')

    for link in telemarket24_links:
        response = requests.get(link)

        if response.status_code != 200:
            logging.error(f'Ошибка запроса для telemarket24.ru: {link}; пропускаю...')
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        for product_elem in soup.find_all('a', class_='link'):
            product_link = product_elem.get('href')
            file_name = f"{project_path}/config/telemarket24-urls.txt"
            full_link = f'https://telemarket24.ru{product_link}'
            if '.html' not in full_link:
                continue

            with open(file_name, 'r') as file:
                content = file.read()
                if full_link in content:
                    continue
                else:
                    with open(file_name, 'a') as file_a:
                        file_a.write(f"\n{full_link}")

    logging.info(f'Ссылки для telemarket24.ru собраны')
