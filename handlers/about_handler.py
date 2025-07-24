from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message


from apideal import get_order_list, get_order
from scripts import get_last_order_from_db, add_order_to_db

router = Router()

@router.message(Command('about','alexkarden'))
async def cmd_about(message: Message):
    about_text = 'Бот написан Alex Karden - https://github.com/alexkarden'
    await message.answer(about_text, parse_mode=ParseMode.HTML)








