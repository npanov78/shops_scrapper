import logging

from config.config import lite_mobile_url
from scripts.no_bitrix_db import sync_no_bitrix_db
from scripts.no_bitrix_db_async import sync_no_bitrix_db_async
from scripts.parse_file import read_urls
from scripts.xml import read_file_from_url, parse_xml_and_update_db


def start_lite_mobile_scrap():
    """
    Функция запускает сканирование цен на сайте lite-mobile.ru
    """
    logging.info(f'Начинаю сканировать lite-mobile.ru')
    urls = read_urls('lite-mobile')
    sync_no_bitrix_db(urls, 'lite-mobile')
    # xml_content = read_file_from_url(lite_mobile_url)
    # if xml_content is None:
    #     logging.error(f'Ошибка получения данных с сайта lite-mobile.ru!')
    #     return 0
    #
    # parse_xml_and_update_db(xml_content, 'lite-mobile')
    logging.info("Данные lite-mobile.ru успешно синхронизированы.")


async def start_lite_mobile_scrap_async():
    """
    Функция запускает сканирование цен на сайте lite-mobile.ru
    """
    logging.info(f'Начинаю сканировать lite-mobile.ru')
    urls = read_urls('lite-mobile')
    await sync_no_bitrix_db_async(urls, 'lite-mobile')
    logging.info("Данные lite-mobile.ru успешно синхронизированы.")
