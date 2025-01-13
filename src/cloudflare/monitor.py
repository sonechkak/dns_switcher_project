import time

import requests
from src.cloudflare.namespaces import *
from src.cloudflare.logger import logging

MONITORED_SITES = get_data()

async def monitor_site():
    logging.info("Мониторинг сайтов начат")
    while True:
        for site in MONITORED_SITES:
            site_url = f"http://{site['zone']}"
            logging.info(f"Проверка сайта: {site_url}")
            try:
                response = requests.get(site_url)
                logging.info(f"Статус ответа: {response.status_code}")
                if response.status_code == 200:
                    logging.info(f"Сайт {site_url} доступен")
                    site["counter"] = 0
            except requests.exceptions.ConnectionError:
                    logging.info(f"Сайт {site_url} недоступен")
                    await update_site_counter(site)

        time.sleep(CHECK_INTERVAL_SECONDS)
