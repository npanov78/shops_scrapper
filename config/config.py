import os

timeout = int(os.getenv("TIMEOUT", 60 * 5))  # default таймаут 5 минут
allow_async = int(os.getenv("ALLOW_ASYNC", 0))
project_path = os.getenv("PROJECT_PATH")
if project_path is None:
    exit('Переменаня окружения PROJECT_PATH пустая!')

TELEGRAM_TOKEN = '**********:*************************************'

chats = ['*********', '*********', '*********', '*********'] # вставь id пользователй, которым хочешь дать доступ

# Списки
exclude = os.getenv("EXCLUDE", ['Варочная панель', 'Ubiquiti', 'Установка', 'Подарки'])
white_list = os.getenv("WHITE_LIST", [])

no_xml_sellers = ['gsmbutik', 'world-devices', 'telemarket24', 'advanced-tech', 'kasla', 'lite-mobile', 'mobilewood', 'pitergsm']

