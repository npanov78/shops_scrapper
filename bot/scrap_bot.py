import asyncio
import logging
import os
import re
import sqlite3
from datetime import datetime

import requests
from reportlab.lib.pagesizes import letter
from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph

project_path = os.getenv("PROJECT_PATH")
if project_path is None:
    exit('Переменаня окружения PROJECT_PATH пустая!')

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(f'{project_path}/log/bot.log'),
              logging.StreamHandler()]
)

TELEGRAM_TOKEN = '6901416401:AAGhwfdCpbPCYIoeNzC2Q3mfSWSWnKrV0MM'
chats = ['582405054', '5183719018', '382290061', '6316631465']
no_xml_sellers = ['gsmbutik', 'world-devices', 'telemarket24', 'advanced-tech', 'kasla', 'lite-mobile', 'mobilewood', 'pitergsm']

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

conn = sqlite3.connect(f'{project_path}/db/bot.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS white_list (
        chat_id INTEGER PRIMARY KEY,
        words TEXT,
        disturb_always INTEGER
    )
''')
conn.commit()


def white_list_keyboard():
    kb = [
        [types.InlineKeyboardButton(callback_data='add_word', text="Добавить слово")],
        [types.InlineKeyboardButton(callback_data='delete_word', text="Удалить слово")],
        [types.InlineKeyboardButton(callback_data='list_words', text="Вывести все слова")],
        [types.InlineKeyboardButton(callback_data='delete_all_words', text="Удалить все слова")],
        [types.InlineKeyboardButton(callback_data='menu', text="Меню")]

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def disturb_keyboard():
    kb = [
        [types.InlineKeyboardButton(callback_data='enable_disturb_always', text="Выключить")],
        [types.InlineKeyboardButton(callback_data='disable_disturb_always', text="Включить")],
        [types.InlineKeyboardButton(callback_data='menu', text="Меню")]

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def main_keyboard():
    kb = [
        [types.InlineKeyboardButton(callback_data='help', text="Помощь")],
        [types.InlineKeyboardButton(callback_data='add_link', text="Добавить ссылку")],
        [types.InlineKeyboardButton(callback_data='white_list', text="Белый список")],
        [types.InlineKeyboardButton(callback_data='disturb_always', text="Режим не беспокоить")],
        [types.InlineKeyboardButton(callback_data='search', text="Поиск")]

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@dp.message(Command('start'))
async def start_command(message: types.Message):
    logging.warning(f'Пользователь {message.from_user.id} подключился к боту')
    if str(message.chat.id) not in chats:
        await bot.send_message(chat_id=message.chat.id, text="Тебе не рады в этом боте")
        logging.error(f'Пользователю {message.from_user.id} отказан доступ')
    else:
        await message.reply(f'Привет, {message.from_user.full_name}!',
                            reply_markup=main_keyboard())


@dp.callback_query(lambda c: c.data == 'help')
async def process_help(callback_query: types.CallbackQuery):
    help_message = """
    <b>Добавить ссылку</b>
    Для магазинов пришлите ссылку на товар, который хотите отслеживать.  После добавления нового товара необходимо добавить ключевое слово в белый список. Также можно просто отправить ссылку боту, чтобы занести ее в базу.
    
    <b>Поддерживаю магазины</b>
    • gsmbutik
    • telemarket24
    • world-devices 
    • advanced-tech 
    • kasla
    • mobilewood 
    • pitergsm
    • lite-mobile 
    
    <b>Белый список</b>
    Набор ключевых слов, которые входят в полное имя товара. Уведомления будут отправляться только для товаров, у которых в названии есть слова из белого списка. Поэтому указывайте названия максимально в общем виде, например: xiaomi, honor, iphone. Для добавления введите /add "слово", например /add xiaomi

    <b>Режим не беспокоить</b>
    При выключенном режиме уведомления будут приходить всегда. 
    При включенном уведомления не будут приходить ночью с 22:00 до 10:00 во время рабочей недели, а также не будут в Сб и Вс.
    
    <b>Поиск</b>
    Режим поиска позиций по ключевым словам. Выбираются все позиции для каждого магазина, где встречаются ключевые введеные слова, и создается PDF отчет. Введи /search "набор аргументов", например /search samsung s24 ultra 512 onyx

    """
    await callback_query.answer()
    await callback_query.message.answer(help_message, parse_mode='HTML', reply_markup=main_keyboard())


@dp.message(Command('menu'))
async def menu_message_link(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Выберите действие:", reply_markup=main_keyboard())


@dp.callback_query(lambda c: c.data == 'menu')
async def menu_link(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Выберите действие:", reply_markup=main_keyboard())


@dp.callback_query(lambda c: c.data == 'add_link')
async def process_add_link(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Введи ссылку:")


@dp.message(lambda message: message.text.startswith('https://'))
async def process_received_link(message: types.Message):
    seller_name_match = re.match(r'https://(.+?)\.(ru|com)/', message.text)
    if seller_name_match:
        seller_name = seller_name_match.group(1)
        if seller_name not in no_xml_sellers:
            await message.answer("Некорректный сайт. Посмотри раздел Помощь.")
        else:
            file_name = f"{project_path}/config/{seller_name}-urls.txt"

            with open(file_name, 'r') as file:
                content = file.read()
                if message.text in content:
                    await bot.send_message(chat_id=message.chat.id, text="Ссылка уже существуюет")
                else:
                    with open(file_name, 'a') as file_a:
                        file_a.write(f"\n{message.text}")
                        logging.warning(f'Добавлена ссылка {message.text}')
                        await message.answer(f"Ссылка добавлена для продавца {seller_name}")


@dp.callback_query(lambda c: c.data == 'white_list')
async def process_white_list(callback_query: types.CallbackQuery):
    await callback_query.answer()
    keyboard = white_list_keyboard()
    await callback_query.message.answer("Белый список: выбери действие", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data in ['add_word', 'delete_word', 'list_words', 'delete_all_words'])
async def process_white_list_actions(callback_query: types.CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id

    if action == 'add_word':
        await callback_query.message.answer("Введите слово для добавления в белый список, начиная с /add:")

    elif action == 'delete_word':
        cursor.execute("SELECT words FROM white_list WHERE chat_id = ?", (user_id,))
        words = cursor.fetchone()[0].split(',')
        kb = []
        for word in words:
            kb.append([types.InlineKeyboardButton(callback_data=f"delete_{word}", text=f"{word}")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await callback_query.message.answer("Выбери слово для удаления из белого списка:", reply_markup=keyboard)

    elif action == 'list_words':
        # Получаем список слов из базы данных
        cursor.execute("SELECT words FROM white_list WHERE chat_id = ?", (user_id,))
        words = cursor.fetchone()[0]
        await bot.send_message(chat_id=user_id, text=f"В твоем белом списке находятся следующие слова:\n {words[:-1]}",
                               reply_markup=white_list_keyboard())

    elif action == 'delete_all_words':
        cursor.execute("UPDATE white_list SET words = '' WHERE chat_id = ?", (user_id,))
        conn.commit()
        await bot.send_message(chat_id=user_id, text="Все слова из твоего белого списка удалены.",
                               reply_markup=white_list_keyboard())


@dp.callback_query(lambda c: c.data.startswith('delete_'))
async def process_delete_word(callback_query: types.CallbackQuery):
    word = callback_query.data[7:]
    user_id = callback_query.from_user.id
    cursor.execute("SELECT words FROM white_list WHERE chat_id = ?", (user_id,))
    words = cursor.fetchone()[0].split(',')
    words.remove(word)
    cursor.execute("UPDATE white_list SET words = ? WHERE chat_id = ?", (','.join(words), user_id))
    conn.commit()
    await bot.send_message(chat_id=user_id, text=f"Слово {word} удалено из твоего белого списка.",
                           reply_markup=white_list_keyboard())


@dp.message(lambda message: message.text.startswith('/add'))
async def process_add_word(message: types.Message):
    word = message.text.replace('/add', '')
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM white_list WHERE chat_id = ?", (user_id,))
    record = cursor.fetchone()
    if record is None:
        cursor.execute("INSERT INTO white_list (chat_id, words, disturb_always) VALUES (?, '', 0)", (user_id,))
        conn.commit()
    cursor.execute("UPDATE white_list SET words = words || ? WHERE chat_id = ?", (' ' + word + ',', user_id))
    conn.commit()
    await bot.send_message(chat_id=user_id, text=f"Слово {word} добавлено в твой белый список.",
                           reply_markup=white_list_keyboard())


@dp.callback_query(lambda c: c.data == 'disturb_always')
async def process_white_list(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    cursor.execute("SELECT * FROM white_list WHERE chat_id = ?", (user_id,))
    record = cursor.fetchone()
    if record is None:
        cursor.execute("INSERT INTO white_list (chat_id, words, disturb_always) VALUES (?, '', 0)", (user_id,))
        conn.commit()
    cursor.execute("SELECT disturb_always FROM white_list WHERE chat_id = ?", (user_id,))
    disturb_always_state = cursor.fetchone()[0]
    if disturb_always_state:
        ne_bespokoit = 'выключен ❌'
    else:
        ne_bespokoit = 'включен ✅'
    await bot.send_message(chat_id=user_id, text=f"Режим не беспокоить {ne_bespokoit}",
                           reply_markup=disturb_keyboard())


@dp.callback_query(lambda c: c.data in ['enable_disturb_always', 'disable_disturb_always'])
async def process_disturb_always_actions(callback_query: types.CallbackQuery):
    action = callback_query.data
    user_id = callback_query.from_user.id
    if action == 'enable_disturb_always':
        cursor.execute("UPDATE white_list SET disturb_always = 1 WHERE chat_id = ?", (user_id,))
        conn.commit()
        await bot.send_message(chat_id=user_id, text=f"Режим не беспокоить выключен",
                               reply_markup=main_keyboard())
    elif action == 'disable_disturb_always':
        cursor.execute("UPDATE white_list SET disturb_always = 0 WHERE chat_id = ?", (user_id,))
        conn.commit()
        await bot.send_message(chat_id=user_id, text=f"Режим не беспокоить включен",
                               reply_markup=main_keyboard())


@dp.callback_query(lambda c: c.data == 'search')
async def process_white_list(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Поиск товара: введите /search аргументы")


def add_text_with_line_breaks(pdf, x, y, text, max_line_length=600):
    lines = []
    words = text.split()

    current_line = ""
    for word in words:
        if pdf.stringWidth(f"{current_line} {word}", "DejaVuSans", 12) <= max_line_length:
            current_line += f"{word} "
        else:
            lines.append(current_line.strip())
            current_line = f"{word} "

    if current_line:
        lines.append(current_line.strip())

    for line in lines:
        pdf.drawString(x, y, line)
        y -= 20  # Adjust the line spacing as needed


@dp.message(lambda message: message.text.startswith('/search'))
async def search_base(message: types.Message):
    user_id = message.from_user.id

    await bot.send_message(chat_id=user_id, text=f"Начинаю делать отчет...")

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_filename = f"{project_path}/db/{user_id}-{current_time}.pdf"

    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Russian', fontName='DejaVuSans'))

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    command_parts = message.text.split()
    search_args = command_parts[1:]
    elements.append(Paragraph(f"Аргументы поиска: {' '.join(search_args)}", styles['Russian']))

    for db_name in no_xml_sellers:
        conn = sqlite3.connect(f"{project_path}/db/{db_name}.db")
        cursor = conn.cursor()

        query = "SELECT clear_name, price FROM offers WHERE "
        for arg in search_args:
            query += f"clear_name LIKE '%{arg}%' AND "
        query = query[:-4]

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            continue

        conn.close()

        elements.append(Paragraph(f"<br/><b>Сайт: {db_name}.ru</b><br/>", styles['Russian']))

        for result in results:
            elements.append(Paragraph(f"{result[0]} - {result[1]} руб.<br/>", styles['Russian']))

    doc.build(elements)

    method = "sendDocument"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    files = {'document': open(pdf_filename, 'rb')}
    data = {'chat_id': user_id}
    response = requests.post(url, files=files, data=data)

    if response.status_code != 200:
        logging.error(f'Ошибка отправки отчета')
        await bot.send_message(chat_id=user_id, text=f"Ошибка создания отчета")
    else:
        logging.warning(f'Отчет {search_args} отправлен пользователю {user_id}')

    os.remove(pdf_filename)

async def main():
    logging.warning(f'Запускаю бота')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
