from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.states import DeleteSearchRequestState
from loader import dp, bot
from database.db_hendler import get_search_user_request


@dp.message_handler(commands='my_search')
async def get_all_search(message: Message):
    my_requests = get_search_user_request(message.chat.id)
    message_text = ''
    for request in my_requests:
        message_text += f'Запрос: {request.text}\nдиапазон цен: {request.price_range}\n\n'

    await bot.send_message(message.chat.id, message_text)
