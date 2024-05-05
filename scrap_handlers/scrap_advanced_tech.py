import logging

from config.config import advanced_tech_url
from scripts.no_bitrix_db import sync_no_bitrix_db
from scripts.no_bitrix_db_async import sync_no_bitrix_db_async
from scripts.parse_file import read_urls
from scripts.xml import read_file_from_url, parse_xml_and_update_db


def start_advanced_tech_scrap():
    """
    Функция запускает сканирование цен на сайте advanced-tech.ru
    """
    logging.info(f'Начинаю сканировать advanced-tech.ru')
    urls = read_urls('advanced-tech')
    sync_no_bitrix_db(urls, 'advanced-tech')
    xml_content = read_file_from_url(advanced_tech_url)
    if xml_content is None:
        logging.error(f'Ошибка получения данных с сайта advanced-tech.ru!')
        return 0

    parse_xml_and_update_db(xml_content, 'advanced-tech')
    logging.info("Данные advanced-tech.ru успешно синхронизированы.")


async def start_advanced_tech_scrap_async():
    """
    Функция запускает сканирование цен на сайте advanced-tech.ru
    """
    logging.info(f'Начинаю сканировать advanced-tech.ru')
    urls = read_urls('advanced-tech')
    await sync_no_bitrix_db_async(urls, 'advanced-tech')
    logging.info("Данные advanced-tech.ru успешно синхронизированы.")
