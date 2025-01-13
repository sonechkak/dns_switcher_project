import os

import aiohttp
import requests
from dotenv import load_dotenv
from src.cloudflare.logger import logging
from src.cloudflare.monitor import MONITORED_SITES
from src.cloudflare.utils.common import get_zones_id

# Загрузка переменных окружения
load_dotenv()

CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')


def check_site_available(site: str) -> bool:
    if not site.startswith(('http://', 'https://')):
        site = 'http://' + site
    try:
        response = requests.get(site)
        logging.info(f"Статус ответа: {response.status_code}")
        if response.status_code == 200:
            logging.info(f"Сайт {site} доступен")
        return True
    except requests.exceptions.ConnectionError:
        logging.error(f"Сайт {site} недоступен")
        return False


def get_zone_id_by_name(zone_name: str) -> str:
    url = "https://api.cloudflare.com/client/v4/zones"
    headers = {
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    logging.info(f"Получаем ID зоны: {zone_name}")
    response = requests.get(url, headers=headers)
    response_data = response.json()
    zone_id = None

    for zone in response_data["result"]:
        if zone["name"] == zone_name:
            zone_id = zone["id"]
            logging.info(f"ZONE_ID: {zone_id}")
            break
    return zone_id


def get_record_id_by_name(zone_id: str, record_name: str) -> str:
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    logging.info(f"Получаем ID записи: {record_name}")
    response = requests.get(url, headers=headers)
    response_data = response.json()
    record_id = None

    for record in response_data["result"]:
        if record["name"] == record_name:
            record_id = record["id"]
            logging.info(f"Получили id записи: {record['id']}")
        else:
            logging.error(f"Ошибка: {response_data}")
    return record_id


def get_record_ip_by_id(zone_id: str, record_id: str) -> str:
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    logging.info(f"Получаем IP записи: {record_id}")
    response = requests.get(url, headers=headers)
    response_data = response.json()
    record_ip = None
    if response.status_code == 200:
        record_ip = response_data["result"]["content"]
        logging.info(f"Получили IP записи: {record_ip}")
    else:
        logging.error(f"Ошибка: {response_data}")
    return record_ip


def get_dns_record_type(zone_id: str, record_id: str) -> str:
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    logging.info(f"Получаем тип записи: {record_id}")
    response = requests.get(url, headers=headers)
    response_data = response.json()
    record_type = None
    if response.status_code == 200:
        record_type = response_data["result"]["type"]
        logging.info(f"Получили тип записи: {record_type}")
    else:
        logging.error(f"Ошибка: {response_data}")
    return record_type


async def update_existing_record(zone_id: str, record_id: str, record_name: str, data: dict) -> dict:
    primary_ip = get_record_ip_by_id(zone_id, record_id)
    if primary_ip == data["ips"][0]:
        secondary_ip = data["ips"][1]
    else:
        secondary_ip = data["ips"][0]

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": get_dns_record_type(zone_id, record_id),
        "name": record_name,
        "content": secondary_ip,
        "ttl": 1,
        "proxied": False
    }

    logging.info(f"Обновляем запись: {record_name}")
    logging.info(f"Отправляемые данные: {data}")

    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, json=data) as response:
            try:
                response_data = await response.json()
                logging.info(f"Статус ответа: {response.status}")
                if response.status == 200:
                    logging.info("Запись успешно обновлена")
                else:
                    logging.error(f"Не удалось обновить запись: {response_data}")
            except Exception as e:
                logging.error(f"Произошла ошибкка: {e}")

            return response_data


# F
async def get_all_zones() -> dict:
    url = "https://api.cloudflare.com/client/v4/zones"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code == 200 and response_data.get("success"):
        logging.info("Запрос успешно выполнен")
    else:
        logging.error(f"Не удалось выполнить запрос: {response_data}")
    return response_data


async def get_min_dns_records() -> dict:
    cloudflare_zone_id = get_zones_id(MONITORED_SITES)
    url = f"https://api.cloudflare.com/client/v4/zones/{cloudflare_zone_id}/dns_records/export/"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.text
    result = {"data": response_data}
    if response.status_code == 200:
        logging.info("Запрос успешно выполнен")
    else:
        logging.error(f"Не удалось выполнить запрос: {response_data}")
    return result


async def get_records() -> dict:
    cloudflare_zone_id = get_zones_id(MONITORED_SITES)
    url = f"https://api.cloudflare.com/client/v4/zones/{cloudflare_zone_id}/dns_records/"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code == 200 and response_data.get("success"):
        logging.info("Запрос успешно выполнен")
    else:
        logging.error(f"Не удалось выполнить запрос: {response_data}")
    return response_data

# Fix this
async def delete_record_by_id() -> dict:
    cloudflare_zone_id = get_zones_id(MONITORED_SITES)
    record_id = get_record_id_by_name(cloudflare_zone_id, "test")
    url = f"https://api.cloudflare.com/client/v4/zones/{cloudflare_zone_id}/dns_records/{record_id}"
    headers = {
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    response_data = response.json()
    if response.status_code == 200 and response_data.get("success"):
        logging.info("Запись успешно удалена")
    else:
        logging.error(f"Не удалось удалить запись: {response_data}")
    return response_data
