import logging
import ast

from aiogram import Bot

from apideal import get_order_list, get_order
from scripts import get_last_order_from_db, add_order_to_db, get_order_list_for_rassilka,  change_status_order
from config import LISTOFADMINS



async def update_orders():
    orders = get_order_list()
    last_order = await get_last_order_from_db()
    for order in orders['orders']:
        if last_order < order['id']:
            await add_order_to_db(order['id'], str(get_order(order['id'])))


async def rassilka_for_users(bot: Bot):
    try:
        order_list_for_rassilka = await get_order_list_for_rassilka(0)
        for order in order_list_for_rassilka:
            number_of_orders = order[1]
            data_tuple = ast.literal_eval(order[2])
            # Извлечение данных
            order_details = data_tuple['order']
            order_id = order_details['id']
            client_name = f"{order_details['client_first_name']} {order_details['client_second_name']} {order_details['client_last_name']}".strip()
            email = order_details['email']
            phone = order_details['phone']
            delivery_address = order_details['delivery_address']
            price = order_details['price']
            products = order_details['products']  # Список из продуктов

            # Вывод извлеченных данных
            text = (f"<b>Заказ №: {order_id}</b>\n"
                    f"Стоимость заказа:<b> {price}</b>\n\n")


            # Вывод информации о продуктах
            text = f'{text}<b>Продукты в заказе:</b>\n\n'
            for product in products:
                text = f'{text}{product['name']}\n'
                text = f'{text}Колличество: <b>{product['quantity']} {product['measure_unit']}</b>\n\n'

            for idtg in LISTOFADMINS:
                await bot.send_message(chat_id=idtg, text = text, parse_mode='HTML')

            await change_status_order(1,number_of_orders)

    except Exception as e:
        logging.error(f"Ошибка при рассылке: {e}")