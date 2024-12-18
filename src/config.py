import os
import requests
import logging
import asyncio
from dotenv import load_dotenv
from crud import update_existing_record

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Загрузка переменных окружения
SITE_URL = os.getenv("MONITORED_SITE_URL")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", 5))
FAILURE_COUNT = 0


async def monitor_site():
    global FAILURE_COUNT
    while True:
        try:
            response = requests.get(SITE_URL)
            if response.status_code == 200:
                if response.headers.get('Content-Type') == 'application/json':
                    try:
                        logging.debug(f"Ответ сервера: {response.text}")
                        result = response.json()
                    except requests.exceptions.JSONDecodeError:
                        logging.error("Ошибка декодирования JSON: %s", response.text)
                        result = None
                else:
                    logging.error("Ответ не является JSON: %s", response.text)
                    result = None
            else:
                logging.warning(f"Получен некорректный статус ответа: {response.status_code}")
                result = None

            if result and response.status_code == 200:
                FAILURE_COUNT = 0
            else:
                FAILURE_COUNT += 1
                logging.info(f"Счетчик неудач: {FAILURE_COUNT}")
                if FAILURE_COUNT == 2:
                    await update_existing_record()
                    logging.info("Запись обновлена")
                    FAILURE_COUNT = 0

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(monitor_site())
