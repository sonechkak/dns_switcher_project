import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
MONITORED_SITE_URL = os.getenv("MONITORED_SITE_URL")
DNS_RECORD_NAME = os.getenv("DNS_RECORD_NAMES")


def get_zone_id(monitored_site_url: str) -> str:
    url = f"https://api.cloudflare.com/client/v4/zones/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    for zone_id in response_data["result"]:
        if zone_id["name"] == monitored_site_url:
            zone_id = zone_id["id"]
    return zone_id


CLOUDFLARE_ZONE_ID = get_zone_id(MONITORED_SITE_URL)


def get_record_id(dns_record_name: str) -> str:
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    for record_id in response_data["result"]:
        if record_id["name"] == dns_record_name:
            record_id = record_id["id"]
    return record_id["id"]

# print(get_zone_id(DNS_RECORD_NAME))
# print(get_record_id(MONITORED_SITE_URL))
