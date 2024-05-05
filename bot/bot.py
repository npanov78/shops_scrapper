import datetime
import logging
import sqlite3

import requests
from config.config import TELEGRAM_TOKEN, chats, project_path

conn = sqlite3.connect(f'{project_path}/db/bot.db')
cursor = conn.cursor()


def in_white_list(name: str, user_id: int) -> bool:
    """
    Функция проверяет наличие позиции в white_list.
    :param name: имя позиции
    :return: находится ли позиция в whhite_list
    """
    cursor.execute("SELECT words FROM white_list WHERE chat_id = ?", (user_id,))
    words = cursor.fetchone()[0]
    white_list = words.split(',')[:-1]

    return any(keyword.lower() in name.lower() for keyword in white_list)


def do_not_disturb(disturb_always: int) -> bool:
    """
    Функция определяет текущее время и день недели.
    :return : возврвщает True, если нельзя беспокоить
    и False, если можно
    """
    current_time = datetime.datetime.now().time()
    current_day = datetime.datetime.now().weekday()

    if disturb_always:
        return False

    # Не беспокоить от 22 до 10 и в СБ и ВС
    if ((current_time >= datetime.time(22, 0) or
        current_time < datetime.time(10, 0)) or
            (current_day == 5 or current_day == 6)):
        return True
    else:
        return False


def send_telegram_notification(url_name, new_price, price_before, date_updated, url):
    """
    Функция отправляет сообщение пользователям с информацией о товаре, чья цена изменилась
    :param url_name: имя товара
    :param new_price: новая цена
    :param price_before: старая цена
    :param date_updated: дата обновления
    :url: url товара
    """

    message = f"Цена для {url_name} обновлена!\n" \
              f"Новая цена: {new_price}\n" \
              f"Предыдущая цена: {price_before}\n" \
              f"Разница: {float(price_before) - float(new_price)}\n" \
              f"Дата обновления: {date_updated}\n" \
              f"Ссылка: {url}"

    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

    for chat in chats:
        try:
            if not in_white_list(url_name, int(chat)):
                return
        except TypeError:
            continue

        cursor.execute("SELECT disturb_always FROM white_list WHERE chat_id = ?", (int(chat),))
        disturb_always = cursor.fetchone()[0]

        if do_not_disturb(disturb_always):
            return

        params = {
            'chat_id': chat,
            'text': message,
            'parse_mode': 'HTML',
        }

        response = requests.post(url, data=params)
        if response.status_code == 200:
            logging.info(f'Сообщение отправлено пользователю {chat}!')
        else:
            logging.error(f'Ошибка отправления пользователю {chat}!')
