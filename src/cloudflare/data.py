import os
from dotenv import load_dotenv

from src.cloudflare.crud import *
from src.cloudflare.logger import logging

load_dotenv()

SITE_MAP = list(map(str, os.getenv("DATA_MAP").split(";")))
COUNTER = int(os.getenv("COUNTER"))


def get_data():
    data = []
    for site in SITE_MAP:
        parts = site.split(":")
        zone = parts[0]
        records = parts[1].split(",")
        ips = parts[2].split(",")
        data.append({
            "zone": zone,
            "records": records,
            "ips": ips,
            "counter": 0
        })
    return data


async def update_site_counter(site: dict):
    logging.info(f"Проверка сайта: {site['zone']}")
    site_zone_id = get_zone_id_by_name(site["zone"])
    for record_name in site["records"]:
        logging.info(f"Проверка записи: {record_name}")
        record_id = get_record_id_by_name(site_zone_id, record_name)
        if check_site_available(site["zone"]):
            logging.info(f"Сайт {site['zone']} доступен")
            site["counter"] = 0
        else:
            logging.info(f"Сайт {site['zone']} недоступен. Увеличиваем счетчик")
            site["counter"] += 1
            logging.info(f"Счетчик: {site['counter']}")
            if site["counter"] == COUNTER:
                logging.info(f"Сайт {site['zone']} недоступен более {COUNTER} раз. Обновляем запись")
                await update_existing_record(site_zone_id, record_id, record_name, site)
                site["counter"] = 0
