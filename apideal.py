import requests
import logging
import os
from config import API_URL
from dotenv import load_dotenv
load_dotenv()




def make_request(url):
    headers = {'Authorization': 'Bearer ' + os.getenv("AUTH_TOKEN"),
               'Content-type': 'application/json'}
    try:
        response = requests.get(API_URL+url, headers=headers)  # Используйте requests.get для простоты
        response.raise_for_status()  # Проверка для HTTP ошибок (например, 404, 500 и т.д.)
        x = response.json()  # Получаем JSON ответ от сервера
        return x
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")  # Вывод ошибки для отладки
    except Exception as err:
        logging.error(f"An error occurred: {err}")  # Общая обработка исключений



def get_order_list():
    url = '/api/v1/orders/list'
    return make_request(url)


def get_order(order_id):
    url = f'/api/v1/orders/{order_id}'
    return make_request(url)


