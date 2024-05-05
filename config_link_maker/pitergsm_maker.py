import logging
import requests
from bs4 import BeautifulSoup
from config.config import project_path
from config_link_maker.links import pitergsm_links


def configure_pitergsm():
    logging.info(f'Начинаю собирать ссылки для pitergsm.ru')
    for link in pitergsm_links:
        response = requests.get(link)

        if response.status_code != 200:
            logging.error(f'Ошибка запроса для pitergsm.ru: {link}; пропускаю...')
            continue
        soup = BeautifulSoup(response.text, 'html.parser')

        for product_elem in soup.find_all('a', class_='prod-card__link'):
            product_link = product_elem['href']

            file_name = f"{project_path}/config/pitergsm-urls.txt"
            link = f'https://pitergsm.ru{product_link}'

            with open(file_name, 'r') as file:
                content = file.read()
                if link in content:
                    continue
                else:
                    with open(file_name, 'a') as file_a:
                        file_a.write(f"\n{link}")

    logging.info(f'Ссылки для pitergsm.ru собраны')
