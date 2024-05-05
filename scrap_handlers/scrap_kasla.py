import logging

from config.config import lite_mobile_url
from scripts.no_bitrix_db import sync_no_bitrix_db
from scripts.no_bitrix_db_async import sync_no_bitrix_db_async
from scripts.parse_file import read_urls
from scripts.xml import read_file_from_url, parse_xml_and_update_db


def start_kasla_scrap():
    """
    Функция запускает сканирование цен на сайте kasla.ru
    """
    logging.info(f'Начинаю сканировать kasla.ru')
    urls = read_urls('kasla')
    sync_no_bitrix_db(urls, 'kasla')
    # xml_content = read_file_from_url(lite_mobile_url)
    # if xml_content is None:
    #     logging.error(f'Ошибка получения данных с сайта kasla.ru!')
    #     return 0
    #
    # parse_xml_and_update_db(xml_content, 'kasla')
    logging.info("Данные kasla.ru успешно синхронизированы.")


async def start_kasla_scrap_async():
    """
    Функция запускает сканирование цен на сайте kasla.ru
    """
    logging.info(f'Начинаю сканировать kasla.ru')
    urls = read_urls('kasla')
    await sync_no_bitrix_db_async(urls, 'kasla')
    logging.info("Данные kasla.ru успешно синхронизированы.")
