import asyncio
import os
import logging
import time

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.cloudflare.namespaces import update_existing_record

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Загрузка переменных окружения
SITE_MAP = os.getenv("DATA_MAP")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS"))
FAILURE_COUNT = 0


# URL сайта, который необходимо мониторить
def monitored_sites():
    sites = []
    for site in SITE_MAP.split(";"):
        site = site.split(":")[0]
        sites.append(site)
    return sites


def record_names() -> object:
    records = []
    for site in SITE_MAP.split(";"):
        record = site.split(":")[1]
        records.append(record)
    return records


async def monitor_site():
    global FAILURE_COUNT
    while True:
        try:
            for site in monitored_sites():
                site = f"http://{site}"
                response = requests.get(site)
                logging.info(f"Проверка сайта: {site}")
                if response.status_code == 200:
                    logging.info(f"Сайт доступен: {site}")
                    result = True
                else:
                    logging.warning(f"Получен некорректный статус ответа: {response.status_code}")
                    result = None

                if result is None and response.status_code != 200:
                    FAILURE_COUNT += 1
                    logging.info(f"Счетчик неудач: {FAILURE_COUNT}")
                    if FAILURE_COUNT == 5:
                        await update_existing_record()
                        FAILURE_COUNT = 0

            time.sleep(CHECK_INTERVAL_SECONDS)

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
            time.sleep(CHECK_INTERVAL_SECONDS)
