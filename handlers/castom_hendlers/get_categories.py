from aiogram.types import Message
from loader import dp
from parsing.get_categories import parsing_categories


@dp.message_handler(commands='get_categories')
async def my_search(message: Message):
    parsing_categories()
