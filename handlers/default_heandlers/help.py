from aiogram.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot, dp


@dp.message_handler(commands=['help'])
async def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    await bot.send_message(message.from_user.id, '\n'.join(text))
