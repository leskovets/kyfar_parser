from aiogram.types import Message
from loader import dp, bot
from database.db_hendler import get_advertisement


@dp.message_handler(commands='my_advertisements')
async def my_search(message: Message):
    text = ''
    for advertisement in get_advertisement(message.chat.id):
        text += f'{advertisement.title} {advertisement.price} {advertisement.advertisement_id}\n'

    await bot.send_message(chat_id=message.chat.id, text=text)
