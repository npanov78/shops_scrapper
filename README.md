## Scrapper сайтов
Скраппер собирает цены на товары с сайтов магазинов, заносит их в базы данных и мониторит обновление цен, при обновлении отправляет сообщение в телеграм-бот.

Скрапер не будет беспокоить пользователей с 22 до 10 и по СБ и ВС. Отключить эту функцию можно, используя переменную окружения DISTURB_ALWAYS.

Скрапер может работать со слежующими сайтами:
1. https://advanced-tech.ru
2. https://kasla.ru
3. https://lite-mobile.ru
4. https://mobilewood.com
5. https://world-devices.ru
6. https://gsmbutik.ru
7. https://telemarket24.ru
8. https://pitergsm.ru

---
## Запуск проекта

Перед запуском проекта необходимо правильно настроить переменные окружения!!!

Запуск локально без контейнеров:

1. ```python3 -m pip install -r requirements.txt``` - установка зависимостей
2. ```python3 main.py``` или ```python3 main_async.py``` - запуск сервиса мониторинга цен
3. ```python3 bot/scrap_bot.py``` - запуск сервиса бота
4. ```python3 config_link_maker/main_link_maker.py``` - запуск сервиса обновления ссылок

Запсук локалько в контейнере:

1. ```docker compose -f docker/docker-compose-dev.yml up```
---

## Переменные окружения
- ```TIMEOUT=300``` - время сна после синхронизации; default таймаут 5 минут
- ```EXCLUDE=['iphone']``` - черный список, что не будет обрабатывать скраппер; default ['Варочная панель', 'варочная панель']. Регистр вводимых имен позиций не важен. Код сведет все к нижнему регистру.

- ```PROJECT_PATH=/home/user/scrap``` - переменная указывает путь до проекта
- ```ALLOW_ASYNC=1``` - переменная, которая разрешает многопоточный режим работы. Не на всех устройствах может рабоатть корректно.


---
## Реализованные сервисы

1. Сборщик ссылок. Собирает и актуализирует ссылки в config/{site}-urls.txt
2. Скраппер страниц, обновлющий цены в БД
3. Телеграм бот для фильтрации уведомлений и работы с БД


Работа со скраппером происходит напрямую через бота. Задаются статически id пользователей, кто имеет доступ до бота. Для каждого пользовтаеля создается запись в БД с белым списком и настройкой режима не беспокоить.