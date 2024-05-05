import logging
import time
from scrap_handlers.scrap_advanced_tech import start_advanced_tech_scrap
from scrap_handlers.scrap_mobilewood import start_mobilewood_scrap
from scrap_handlers.scrap_lite_mobile import start_lite_mobile_scrap
from scrap_handlers.scrap_kasla import start_kasla_scrap
from config.config import timeout, exclude, project_path
from scrap_handlers.scrap_pitergsm import start_pitergsm_scrap
from scrap_handlers.scrap_world_devices import start_world_devices_scrap
from scrap_handlers.scrap_gsmbutik import start_gsmbutik_scrap
from scrap_handlers.scrap_telemarket24 import start_telemarket24_scrap

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(f'{project_path}/log/scrapper.log'),
              logging.StreamHandler()]
)


if __name__ == "__main__":
    logging.info(f'Начинаю работу')
    logging.info(f'Ban лист: {exclude}')

    try:
        while True:
            start_mobilewood_scrap()
            start_kasla_scrap()
            start_advanced_tech_scrap()

            start_lite_mobile_scrap()


            start_pitergsm_scrap()
            start_gsmbutik_scrap()
            start_telemarket24_scrap()
            start_world_devices_scrap()
            logging.info(f"Засыпаю на {int(timeout / 60)} минут")
            time.sleep(timeout)
    except KeyboardInterrupt or Exception as e:
        logging.info(f'Завершаю работу скраппера. {e}')