import logging
from scripts.no_bitrix_db import sync_no_bitrix_db
from scripts.no_bitrix_db_async import sync_no_bitrix_db_async
from scripts.parse_file import read_urls


def start_gsmbutik_scrap():
    """
    Функция запускает работу скрапера gsmbutik.ru.
    считываются url из конфиг файла и для каждой ссылки
    выполянется синхронизация.
    """
    urls = read_urls('gsmbutik')
    sync_no_bitrix_db(urls, 'gsmbutik')
    logging.info(f'Данные gsmbutik.ru успешно синхронизированы.')


async def start_gsmbutik_scrap_async():
    """
    Функция запускает работу скрапера gsmbutik.ru.
    считываются url из конфиг файла и для каждой ссылки
    выполянется синхронизация.
    """
    urls = read_urls('gsmbutik')
    await sync_no_bitrix_db_async(urls, 'gsmbutik')
    logging.info(f'Данные gsmbutik.ru успешно синхронизированы.')
