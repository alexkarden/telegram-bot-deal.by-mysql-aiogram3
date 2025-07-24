import logging
import aiomysql

from config import host, user, password, port, db_name

DATABASE_CONFIG = {
    'host': host,        # хост MySQL (обычно localhost)
    'port': port,               # порт (обычно 3306)
    'user': user,    # имя пользователя
    'password': password, # пароль
    'db': db_name,      # имя базы данных
}


# Создает и возвращает пул соединений к базе данных.--------------------------------------------------------------------mySQL
async def create_pool():
    return await aiomysql.create_pool(**DATABASE_CONFIG)


# Инициализация базы данных---------------------------------------------------------------------------------------------mySQL
async def init_db():
    pool = None  # Объявляем переменную для пула соединений
    try:
        pool = await create_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Создание таблицы
                await cursor.execute(
                    "CREATE TABLE IF NOT EXISTS orders ("
                    "id INT AUTO_INCREMENT PRIMARY KEY, "
                    "number_of_order INT UNIQUE NOT NULL, "
                    "order_text LONGTEXT, "  # Указан максимальный размер VARCHAR
                    "send_status INT NOT NULL, "
                    "resend_status INT NOT NULL)"
                )
                await conn.commit()
    except aiomysql.MySQLError as e:
        logging.error(f"Ошибка при работе с MySQL - Инициализация базы данных: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        # Закрываем пул соединений, если он был создан
        if pool:
            pool.close()
            await pool.wait_closed()

# Добавление заказа в базу данных --------------------------------------------------------------------------------------mySQL
async def add_order_to_db(number_of_order, order_text):
    send_status = 0
    resend_status = 0
    pool = None  # Объявляем переменную для пула соединений
    try:
        pool = await create_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO orders (number_of_order, order_text, send_status, resend_status) VALUES (%s, %s, %s, %s);",
                    (number_of_order, order_text, send_status, resend_status))
            await conn.commit()
    except aiomysql.MySQLError as e:
        logging.error(f"Ошибка при работе с MySQL: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        # Закрываем пул соединений, если он был создан
        if pool:
            pool.close()
            await pool.wait_closed()

# Получение последнего заказа из базы данных ---------------------------------------------------------------------------mySQL
async def get_last_order_from_db():
    pool = None  # Объявляем переменную для пула соединений
    try:
        pool = await create_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT MAX(number_of_order) FROM orders")
                result = await cursor.fetchone()
                if result and result[0] is not None:
                    last_order_number = result[0]
                else:
                    last_order_number = 0  # Если нет заказов, возвращаем 0
                    logging.info("В таблице заказов нет записей. Возвращаем номер заказа равный 0.")
                return last_order_number
    except aiomysql.MySQLError as e:
        logging.error(f"Ошибка при работе с MySQL - Получение последнего заказа из базы данных: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        # Закрываем пул соединений, если он был создан
        if pool:
            pool.close()
            await pool.wait_closed()

# Получение списка заказов из базы данных для рассылки -----------------------------------------------------------------mySQL
async def get_order_list_for_rassilka(status):
    pool = None  # Объявляем переменную для пула соединений
    try:
        pool = await create_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Получаем все заказы из таблицы, которые надо разослать
                await cursor.execute("SELECT * FROM orders WHERE send_status = %s", (status,))
                result = await cursor.fetchall()
                return result
    except aiomysql.MySQLError as e:
        logging.error(f"Ошибка при работе с MySQL - Получение списка заказов из базы данных для рассылки: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        # Закрываем пул соединений, если он был создан
        if pool:
            pool.close()
            await pool.wait_closed()

# Смена статуса заказа для рассылки-------------------------------------------------------------------------------------mySQL
async def change_status_order(send_status, number_of_orders):
    pool = None  # Объявляем переменную для пула соединений
    try:
        pool = await create_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Обновляем статус заказа
                await cursor.execute(
                    "UPDATE orders SET send_status = %s WHERE number_of_order = %s",
                    (send_status, number_of_orders)
                )
            await conn.commit()  # Выполняем коммит изменений
    except aiomysql.MySQLError as e:
        logging.error(f"Ошибка при работе с MySQL - Смена статуса заказа для рассылки: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        if pool:
            pool.close()
            await pool.wait_closed()


















