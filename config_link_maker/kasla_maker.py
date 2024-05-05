import logging
import requests
from bs4 import BeautifulSoup
from config.config import project_path
from config_link_maker.links import kasla_links


def configure_kasla():
    logging.info(f'Начинаю собирать ссылки для kasla.ru')
    for link in kasla_links:
        response = requests.get(link)

        if response.status_code != 200:
            logging.error(f'Ошибка запроса для kasla.ru: {link}; пропускаю...')
            continue
        soup = BeautifulSoup(response.text, 'html.parser')

        for product_elem in soup.find_all('a', class_='name'):
            product_link = product_elem['href']
            product_name = product_elem.text.strip()
            if product_name == '':
                continue
            file_name = f"{project_path}/config/kasla-urls.txt"
            link = f'https://kasla.ru{product_link}'

            with open(file_name, 'r') as file:
                content = file.read()
                if link in content:
                    continue
                else:
                    with open(file_name, 'a') as file_a:
                        file_a.write(f"\n{link}")

    logging.info(f'Ссылки для kasla.ru собраны')
