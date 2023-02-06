from aiogram.types import Message

from loader import bot, dp


@dp.message_handler(commands=['start'])
async def bot_start(message: Message):
    await bot.send_message(message.from_user.id, f"Привет, {message.from_user.full_name}!")

