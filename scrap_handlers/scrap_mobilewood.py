import logging

from config.config import mobilewood_url
from scripts.no_bitrix_db import sync_no_bitrix_db
from scripts.no_bitrix_db_async import sync_no_bitrix_db_async
from scripts.parse_file import read_urls
from scripts.xml import read_file_from_url, parse_xml_and_update_db


def start_mobilewood_scrap():
    """
    Функция запускает сканирование цен на сайте mobilewood.com
    """
    logging.info(f'Начинаю сканировать mobilewood.com')
    urls = read_urls('mobilewood')
    sync_no_bitrix_db(urls, 'mobilewood')
    # xml_content = read_file_from_url(mobilewood_url)
    # if xml_content is None:
    #     logging.error(f'Ошибка получения данных с сайта mobilewood.com!')
    #     return 0
    #
    # parse_xml_and_update_db(xml_content, 'mobilewood')
    logging.info("Данные mobilewood.com успешно синхронизированы.")


async def start_mobilewood_scrap_async():
    """
    Функция запускает сканирование цен на сайте mobilewood.com
    """
    logging.info(f'Начинаю сканировать mobilewood.com')
    urls = read_urls('mobilewood')
    await sync_no_bitrix_db_async(urls, 'mobilewood')
    logging.info("Данные mobilewood.com успешно синхронизированы.")
