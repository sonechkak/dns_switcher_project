import os

from dotenv import load_dotenv
from fastapi.openapi.models import ParameterInType

from src.cloudflare.crud import *
from src.cloudflare.logger import logging

load_dotenv()

SITE_MAP = list(map(str, os.getenv("DATA_MAP").split(";")))


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
            if site["counter"] == 5:
                logging.info(f"Сайт {site['zone']} недоступен более 5 раз. Обновляем запись")
                await update_existing_record(site_zone_id, record_id, record_name, site)
                site["counter"] = 0


def monitored_sites():
    return set(site["zone"] for site in get_data())


def sites_records():
    records_set = set()
    for site in get_data():
        for record in site["records"]:
            records_set.add(record)
    return records_set


def record_ips():
    ips_set = set()
    for site in get_data():
        for ip in site["ips"]:
            ips_set.add(ip)
    return ips_set


def counters():
    return {site["zone"]: site["counter"] for site in get_data()}

# ENV
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
DNS_RECORD_TYPE = os.getenv('DNS_RECORD_TYPE')
PRIMARY_IP = os.getenv('PRIMARY_IP')
SECONDARY_IP = os.getenv('SECONDARY_IP')

MONITORED_SITES = list(monitored_sites())
SITES_RECORDS = list(sites_records())
RECORD_IPS = list(record_ips())
COUNTERS = counters()
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS"))
