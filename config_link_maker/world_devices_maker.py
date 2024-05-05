import logging
import requests
from bs4 import BeautifulSoup

from config.config import project_path
from config_link_maker.links import world_devices_links


def configure_world_devices():
    logging.info(f'Начинаю собирать ссылки для world-devices.ru')
    for link in world_devices_links:
        response = requests.get(link)

        if response.status_code != 200:
            logging.error(f'Ошибка запроса для world-devices.ru: {link}; пропускаю...')
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        for product_elem in soup.find_all('a', class_='product-thumb__name'):
            product_link = product_elem.get('href')
            file_name = f"{project_path}/config/world-devices-urls.txt"
            full_link = f'{product_link}'

            with open(file_name, 'r') as file:
                content = file.read()
                if full_link in content:
                    continue
                else:
                    with open(file_name, 'a') as file_a:
                        file_a.write(f"\n{full_link}")

    logging.info(f'Ссылки для world-devices.ru собраны')
