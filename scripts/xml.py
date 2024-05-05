import logging
import urllib.request
import xml
import sqlite3
from datetime import datetime
from lxml import etree
from bot.bot import send_telegram_notification
from config.config import *


def read_file_from_url(url: str) -> xml:
    """
    Функция парсит url и возвращает содержимое файла с ценами
    :param url: юрл сайта
    :return: содержимое файла для yandex
    """
    try:
        with urllib.request.urlopen(url) as response:
            file_content = b''
            while True:
                chunk = response.read(4096)
                if not chunk:
                    break
                file_content += chunk
        return file_content.decode('utf-8')
    except Exception as e:
        logging.error(f"Ошибка при чтении файла: {e}")
        return None


def should_exclude(name: str) -> bool:
    """
    Функция проверяет исключенные позиции.
    :param name: имя позиции
    :return: исключена ли позиция
    """
    return any(keyword.lower() in name.lower() for keyword in exclude)


def parse_xml_and_update_db(xml_content: xml, site_name: str):
    """
    Функция парсит скачанный xml, обновляет БД цен. При изменении цены
    отправляет сообщение телеграм боту
    :param xml_content: файл xml с ценами
    :param site_name: имя сайта, который скраппит
    """
    if xml_content is None:
        return

    conn = sqlite3.connect(f'{project_path}/db/{site_name}.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            url TEXT PRIMARY KEY,
            clear_name TEXT,
            price INTEGER,
            last_updated TEXT
        )
    ''')

    try:
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(xml_content.encode('utf-8'), parser=parser)
    except Exception as e:
        logging.error(f'Ошибка получения xml контента! Пропускаю стадию... {e}')
        raise

    for offer_elem in root.findall('.//offer'):
        url_elem = offer_elem.find('url')
        name_elem = offer_elem.find('name')
        price_elem = offer_elem.find('price')

        if url_elem is None or price_elem is None or name_elem is None:
            continue

        url = url_elem.text.strip()
        clear_name = name_elem.text.strip()
        price = int(price_elem.text.strip())

        if should_exclude(clear_name):
            continue

        cursor.execute('SELECT * FROM offers WHERE url=?', (url,))
        existing_offer = cursor.fetchone()

        if existing_offer is None:
            cursor.execute(
                'INSERT INTO offers (url, clear_name, price, last_updated) VALUES (?, ?, ?, ?)',
                (url, clear_name, price, datetime.now()))
            continue

        existing_price = existing_offer[2]
        if existing_price == price:
            continue

        cursor.execute(
            'UPDATE offers SET price=?, last_updated=? WHERE url=?',
            (price, datetime.now(), url))

        logging.info(f"Цена для {clear_name} обновлена.")
        send_telegram_notification(f"{site_name}.ru " + clear_name,
                                   price,
                                   existing_price,
                                   datetime.now(),
                                   url)
    conn.commit()
    conn.close()
