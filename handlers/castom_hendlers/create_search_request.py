from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.states import CreateSearchRequestState
from loader import dp, bot
from database.db_hendler import add_search_request


@dp.message_handler(commands='create_search')
async def create_search_request(message: Message):
    await CreateSearchRequestState.text.set()
    await bot.send_message(message.chat.id, 'Введи искомые товары через запятую')


@dp.message_handler(state=CreateSearchRequestState.text)
async def get_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    await CreateSearchRequestState.next()
    await bot.send_message(message.chat.id, 'Введи минимальную и максимальную цену товара через запятую')


@dp.message_handler(state=CreateSearchRequestState.price)
async def get_price(message: Message, state: FSMContext):
    async with state.proxy() as data:
        text = data['text']
        price_range = message.text

    await state.finish()
    await bot.send_message(message.chat.id, 'Поиск создан!')
    add_search_request(message.chat.id, text, price_range)
