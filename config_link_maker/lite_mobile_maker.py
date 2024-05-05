import logging
import requests
from bs4 import BeautifulSoup
from config.config import project_path
from config_link_maker.links import lite_mobile_links


def configure_lite_mobile():
    logging.info('Начинаю собирать ссылки для lite-mobile.ru')
    for link in lite_mobile_links:
        response = requests.get(link)

        if response.status_code != 200:
            logging.error(f'Ошибка запроса для lite-mobile.ru: {link}; пропускаю...')
            continue
        soup = BeautifulSoup(response.text, 'html.parser')

        for product_elem in soup.find_all('div', class_='catalog-item__title'):
            a_tag = product_elem.find('a')
            if a_tag:
                product_link = a_tag.get('href')
                product_name = a_tag.text.strip()
                if product_name == '':
                    continue
                file_name = f"{project_path}/config/lite-mobile-urls.txt"
                full_link = f'{product_link}'

                with open(file_name, 'r') as file:
                    content = file.read()
                    if full_link in content:
                        continue
                    else:
                        with open(file_name, 'a') as file_a:
                            file_a.write(f"\n{full_link}")

    logging.info('Ссылки для lite-mobile.ru собраны')
