import asyncio
from datetime import datetime
import logging
import sqlite3
import http.client

http.client._MAXHEADERS = 1000
import aiohttp
from bs4 import BeautifulSoup
from bot.bot import send_telegram_notification
from config.config import project_path
from scripts.parse_file import should_exclude


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def process_url(url, handler, cursor):
    response_text = await fetch(url)

    if response_text is None or response_text == '':
        logging.error(f"Не удалось получить информацию из ссылки {url}; пропускаю ее")
        return

    soup = BeautifulSoup(response_text, 'html.parser')

    name_element = None
    price_element = None

    try:
        if handler == 'gsmbutik':
            name_element = soup.find('h1').get_text(strip=True)
            if should_exclude(name_element):
                return
            price_element = soup.find('div',
                                      class_='catalog-detail-info__cur-price').get_text(
                strip=True)
        elif handler == 'world-devices':
            name_element = soup.find('h1', class_='heading').get_text(strip=True)
            if should_exclude(name_element):
                return
            price_element = soup.find('div', class_='product-page__price').get_text(
                strip=True)
        elif handler == 'telemarket24':
            name_element = soup.find('h1').get_text(strip=True)
            if should_exclude(name_element):
                return
            price_element = soup.find('div', class_='price').get_text(strip=True)
        elif handler == 'advanced-tech':
            name_element = soup.find('h1').get_text(strip=True)
            if should_exclude(name_element):
                return
            price_element = soup.find('div', class_='product-card-price').get_text(
                strip=True)
        elif handler == 'mobilewood':
            name_element = soup.find('div', class_='creditgoods').get_text(
                strip=True)
            if should_exclude(name_element):
                return
            price_element = soup.find('div', class_='creditprice').get_text(
                strip=True)
        elif handler == 'lite-mobile':
            name_element = soup.find('h1').get_text(strip=True)
            if should_exclude(name_element):
                return
            price_element = soup.find('div',
                                      class_='detail-card__price-cur').get_text(
                strip=True)
        elif handler == 'kasla':
            name_element = soup.find('h1').get_text(strip=True)
            if should_exclude(name_element):
                return
            price_element = soup.find('span', class_='priceVal').get_text(
                strip=True).replace('руб.', '')
        elif handler == 'pitergsm':
            name_element = soup.find('h1').get_text(strip=True)
            if should_exclude(name_element):
                return
            price_element = soup.find('span', class_='main-detail-price').get_text(
                strip=True)
    except AttributeError:
        return

    try:
        price_element = int(''.join(filter(str.isdigit, price_element.replace('\n', '').replace('\t', ''))))
    except ValueError:
        return

    if not name_element or not price_element:
        return

    if should_exclude(name_element):
        return

    cursor.execute('SELECT * FROM offers WHERE url=?', (url,))
    existing_offer = cursor.fetchone()

    if existing_offer is None:
        cursor.execute(
            'INSERT INTO offers (url, clear_name, price, last_updated) VALUES (?, ?, ?, ?)',
            (url, name_element, price_element, datetime.now()))
        return

    existing_price = existing_offer[2]
    if existing_price == price_element:
        return

    cursor.execute(
        'UPDATE offers SET price=?, last_updated=? WHERE url=?',
        (price_element, datetime.now(), url))

    logging.info(f"{handler}: Цена для {name_element} обновлена.")
    send_telegram_notification(f"{handler}.ru " + name_element,
                               price_element,
                               existing_price,
                               datetime.now(),
                               url)


async def sync_no_bitrix_db_async(urls, handler):
    conn = sqlite3.connect(f'{project_path}/db/{handler}.db')
    cursor = conn.cursor()

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS offers (
                    url TEXT PRIMARY KEY,
                    clear_name TEXT,
                    price INTEGER,
                    last_updated TEXT
                )
            ''')

    tasks = [process_url(url, handler, cursor) for url in urls]
    await asyncio.gather(*tasks)

    conn.commit()
    conn.close()
