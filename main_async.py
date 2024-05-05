import asyncio
import logging
import time

from scrap_handlers.scrap_advanced_tech import start_advanced_tech_scrap, start_advanced_tech_scrap_async
from scrap_handlers.scrap_mobilewood import start_mobilewood_scrap, start_mobilewood_scrap_async
from scrap_handlers.scrap_lite_mobile import start_lite_mobile_scrap, start_lite_mobile_scrap_async
from scrap_handlers.scrap_kasla import start_kasla_scrap, start_kasla_scrap_async
from config.config import timeout, exclude, project_path, allow_async
from scrap_handlers.scrap_pitergsm import start_pitergsm_scrap, start_pitergsm_scrap_async
from scrap_handlers.scrap_world_devices import start_world_devices_scrap, start_world_devices_scrap_async
from scrap_handlers.scrap_gsmbutik import start_gsmbutik_scrap, start_gsmbutik_scrap_async
from scrap_handlers.scrap_telemarket24 import start_telemarket24_scrap, start_telemarket24_scrap_async
import concurrent.futures

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(f'{project_path}/log/scrapper.log'),
              logging.StreamHandler()]
)


async def main_scrap(handlers):
    tasks = []
    for handler in handlers:
        logging.info(f'Запускаю скраппер {handler}')
        task = handler()
        tasks.append(task)

    await asyncio.gather(*tasks)


async def main():
    try:
        handlers = [
            start_advanced_tech_scrap_async,
            start_mobilewood_scrap_async,
            start_lite_mobile_scrap_async,
            start_kasla_scrap_async,
            start_world_devices_scrap_async,
            start_gsmbutik_scrap_async,
            start_telemarket24_scrap_async,
            start_pitergsm_scrap_async
        ]

        while True:
            await main_scrap(handlers)
            logging.info(f"Засыпаю на {int(timeout / 60)} минут")
            await asyncio.sleep(timeout)
    except KeyboardInterrupt:
        logging.info(f'Завершаю работу скраппера.')


if __name__ == "__main__":
    logging.info(f'Начинаю работу')
    logging.info(f'Ban лист: {exclude}')

    if allow_async:
        logging.info(f'Начинаю многопоточную работу, ALLOW_ASYNC=1')
        try:
            while True:
                asyncio.run(main())
                logging.info(f"Засыпаю на {int(timeout / 60)} минут")
                time.sleep(timeout)
        except KeyboardInterrupt or Exception as e:
            logging.info(f'Завершаю работу скраппера. {e}')

    logging.info(f'Начинаю параллельную работу, ALLOW_ASYNC=0')
    try:
        while True:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(start_advanced_tech_scrap)
                executor.submit(start_mobilewood_scrap)
                executor.submit(start_lite_mobile_scrap)
                executor.submit(start_kasla_scrap)
                executor.submit(start_world_devices_scrap)
                executor.submit(start_gsmbutik_scrap)
                executor.submit(start_telemarket24_scrap)
                executor.submit(start_pitergsm_scrap)

            logging.info(f"Засыпаю на {int(timeout / 60)} минут")
            time.sleep(timeout)
    except KeyboardInterrupt or Exception as e:
        logging.info(f'Завершаю работу скраппера. {e}')