from aiogram.types import Message
from aiogram.utils.markdown import hlink

from loader import bot, dp
from parsing.kyfar import get_advertisements


@dp.message_handler(commands=['search'])
async def bot_start(message: Message):

    text = 'partybox 310, party box 310, partybox 300, party box 300'
    price_range = '300,1200'

    for advertisement in get_advertisements(text=text, price_range=price_range):
        text = hlink(advertisement['title'], advertisement['linc'])
        text += ' Цена: '
        text += str(advertisement['price']) if not advertisement['price'] == 0 else 'Договорная'

        await bot.send_message(message.chat.id, text, parse_mode='HTML')

