import logging
from scripts.no_bitrix_db import sync_no_bitrix_db
from scripts.no_bitrix_db_async import sync_no_bitrix_db_async
from scripts.parse_file import read_urls


def start_world_devices_scrap():
    """
    Функция запускает работу скрапера world-devices.ru.
    считываются url из конфиг файла и для каждой ссылки
    выполянется синхронизация.
    """
    urls = read_urls('world-devices')
    sync_no_bitrix_db(urls, 'world-devices')
    logging.info(f'Данные world-devices.ru успешно синхронизированы.')


async def start_world_devices_scrap_async():
    """
    Функция запускает работу скрапера world-devices.ru.
    считываются url из конфиг файла и для каждой ссылки
    выполянется синхронизация.
    """
    urls = read_urls('world-devices')
    await sync_no_bitrix_db_async(urls, 'world-devices')
    logging.info(f'Данные world-devices.ru успешно синхронизированы.')
