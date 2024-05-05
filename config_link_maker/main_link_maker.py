import asyncio
import logging
import concurrent.futures
import time

from config.config import project_path, timeout
from config_link_maker.advanced_tech_link_maker import configure_advanced_tech
from config_link_maker.gsmbutik_link_maker import configure_gsmbutik
from config_link_maker.kasla_maker import configure_kasla
from config_link_maker.lite_mobile_maker import configure_lite_mobile
from config_link_maker.mobilewood_maker import configure_mobilewood
from config_link_maker.pitergsm_maker import configure_pitergsm
from config_link_maker.telemarket24_maker import configure_telemarket24
from config_link_maker.world_devices_maker import configure_world_devices

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(f'{project_path}/log/config_link_maker.log'),
              logging.StreamHandler()]
)


def configure_link_maker(configure_func):
    configure_func()


if __name__ == '__main__':
    logging.info(f'Запускаю обновление ссылок')

    try:
        while True:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(configure_link_maker, func) for func in
                           [
                               configure_mobilewood,
                               configure_telemarket24,
                               configure_world_devices,
                               configure_gsmbutik,
                               configure_lite_mobile,

                               configure_pitergsm,
                               configure_advanced_tech,
                               configure_kasla,
                           ]
                           ]
                concurrent.futures.wait(futures)
                logging.info(f"Засыпаю на {int(timeout * 10 / 60)} минут")
                time.sleep(timeout)
    except KeyboardInterrupt or Exception as e:
        logging.info(f'Завершаю работу скраппера. {e}')
