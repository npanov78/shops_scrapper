import logging
from scripts.no_bitrix_db import sync_no_bitrix_db
from scripts.no_bitrix_db_async import sync_no_bitrix_db_async
from scripts.parse_file import read_urls


def start_pitergsm_scrap():
    """
    Функция запускает сканирование цен на сайте pitergsm.ru
    """
    logging.info(f'Начинаю сканировать pitergsm.ru')
    urls = read_urls('pitergsm')
    sync_no_bitrix_db(urls, 'pitergsm')
    logging.info("Данные pitergsm.ru успешно синхронизированы.")

async def start_pitergsm_scrap_async():
    """
    Функция запускает сканирование цен на сайте pitergsm.ru
    """
    logging.info(f'Начинаю сканировать pitergsm.ru')
    urls = read_urls('pitergsm')
    await sync_no_bitrix_db_async(urls, 'pitergsm')
    logging.info("Данные pitergsm.ru успешно синхронизированы.")
