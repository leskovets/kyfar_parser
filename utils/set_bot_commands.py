from aiogram.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


async def setup_bot_commands(dp):
    commands = [BotCommand(*i) for i in DEFAULT_COMMANDS]
    await dp.bot.set_my_commands(commands)
