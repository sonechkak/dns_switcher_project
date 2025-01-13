import requests
from src.cloudflare.data import *
from src.cloudflare.monitor import MONITORED_SITES


zone_id = None
record_id = None


def get_zones_id(monitored_sites: list) -> str:
    global zone_id
    url = f"https://api.cloudflare.com/client/v4/zones/"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    for zone_id in response_data["result"]:
        if zone_id["name"] in monitored_sites:
            zone_id = zone_id["id"]
    return zone_id


def get_record_id(dns_record_name: str) -> str:
    global record_id
    zone_id = get_zones_id()
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if "result" in response_data and response_data["result"] is not None:
        for record in response_data["result"]:
            if record["name"] == dns_record_name:
                record_id = record["id"]
                break
    else:
        raise ValueError("Invalid response from Cloudflare API or no DNS records found.")

    return record_id
