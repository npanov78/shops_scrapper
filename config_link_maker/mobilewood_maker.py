import logging
import requests
from bs4 import BeautifulSoup
from config.config import project_path
from config_link_maker.links import mobilewood_links


def configure_mobilewood():
    logging.info(f'Начинаю собирать ссылки для mobilewood.com')
    for link in mobilewood_links:
        response = requests.get(link)

        if response.status_code != 200:
            logging.error(f'Ошибка запроса для mobilewood.com: {link}; пропускаю...')
            continue
        soup = BeautifulSoup(response.text, 'html.parser')

        for product_elem in soup.find_all('div', class_='product-header'):
            a_tag = product_elem.find('h3').find('a')
            if a_tag:
                product_link = a_tag.get('href')

                file_name = f"{project_path}/config/mobilewood-urls.txt"
                full_link = f'https://mobilewood.com{product_link}'

                with open(file_name, 'r') as file:
                    content = file.read()
                    if full_link in content:
                        continue
                    else:
                        with open(file_name, 'a') as file_a:
                            file_a.write(f"\n{full_link}")

    logging.info(f'Ссылки для mobilewood.com собраны')
