import os

import logging
import requests
from dotenv import load_dotenv

load_dotenv()

# ENV
CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')
DNS_RECORD_NAMES = os.getenv('DNS_RECORD_NAMES')
DNS_RECORD_TYPE = os.getenv('DNS_RECORD_TYPE')
PRIMARY_IP = os.getenv('PRIMARY_IP')
API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
RECORD_ID = os.getenv('CLOUDFLARE_RECORD_ID')


async def update_existing_record():
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{RECORD_ID}"
    headers = {
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": DNS_RECORD_TYPE,
        "name": DNS_RECORD_NAMES,
        "content": PRIMARY_IP,
        "ttl": 1,
        "proxied": False
    }
    response = requests.put(url, headers=headers, json=data)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("success"):
        logging.info("Запись успешно обновлена")
    else:
        logging.error(f"Не удалось обновить запись: {response_data}")

    return response_data
