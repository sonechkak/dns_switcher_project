import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

def get_zone_id():
    url = f"https://api.cloudflare.com/client/v4/zones/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    return response_data["result"][0]["id"]


CLOUDFLARE_ZONE_ID = str(get_zone_id())


def get_record_id():
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    return response_data["result"][0]["id"]
