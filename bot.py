# Импортируем библиотеку asyncio для работы с асинхронным программированием.
import asyncio
# Импортируем библиотеку для логирования. Позволяет записывать события, ошибки и информацию о работе бота.
import logging
# Импортируем классы Bot и Dispatcher из библиотеки aiogram для создания Telegram-бота.
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# Импортируем токен бота из файла конфигурации config.py
from config import TOKEN_TG, CHECKINTERVAL,CHECKINTERVALR

from scripts import init_db
from scripts_scheduler import update_orders,rassilka_for_users


# Создаем объект Bot, передавая токен, который позволяет боту взаимодействовать с Telegram API.
bot = Bot(token=TOKEN_TG)
# Создаем объект Dispatcher для обработки обновлений и маршрутизации сообщений.
dp = Dispatcher()

# Импортируем роутеры из файлов обработчиков
from handlers.start_handler import router as start_router
from handlers.about_handler import router as about_handler
# Подключаем роутер
dp.include_router(start_router)
dp.include_router(about_handler)



#-----------------------------------------------------------------------------------------------------------------------Основная функция
async def main():
    #Создаем базу данных, если ее нет.
    await init_db()
    #Запускаем проверку цен и рассылку
    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    scheduler.add_job(update_orders, trigger='interval', seconds=CHECKINTERVAL)
    scheduler.add_job(rassilka_for_users, trigger='interval', seconds=CHECKINTERVALR,
                      kwargs={
                          'bot': bot,
                      }
                      )

    # Запускаем шейдулер
    scheduler.start()
    # Запускаем поллинг
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        filename='logfile.log',
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.error('Exit')