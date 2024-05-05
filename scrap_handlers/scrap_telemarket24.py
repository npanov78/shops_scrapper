import logging
from scripts.no_bitrix_db import sync_no_bitrix_db
from scripts.no_bitrix_db_async import sync_no_bitrix_db_async
from scripts.parse_file import read_urls


def start_telemarket24_scrap():
    """
    Функция запускает работу скрапера telemarket24.ru.
    считываются url из конфиг файла и для каждой ссылки
    выполянется синхронизация.
    """
    urls = read_urls('telemarket24')
    sync_no_bitrix_db(urls, 'telemarket24')
    logging.info(f'Данные telemarket24.ru успешно синхронизированы.')


async def start_telemarket24_scrap_async():
    """
    Функция запускает работу скрапера telemarket24.ru.
    считываются url из конфиг файла и для каждой ссылки
    выполянется синхронизация.
    """
    urls = read_urls('telemarket24')
    await sync_no_bitrix_db_async(urls, 'telemarket24')
    logging.info(f'Данные telemarket24.ru успешно синхронизированы.')
