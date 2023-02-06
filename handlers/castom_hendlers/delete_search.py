from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.states import DeleteSearchRequestState
from loader import dp, bot
from database.db_hendler import get_search_user_request, delete_search_request


@dp.message_handler(commands='delete_search')
async def create_search_request(message: Message):
    await DeleteSearchRequestState.select_request.set()
    my_requests = get_search_user_request(message.chat.id)
    message_text = ''
    for request in my_requests:
        message_text += f'Номер: {request.id}\nЗапрос: {request.text}\nдиапазон цен: {request.price_range}\n\n'

    await bot.send_message(message.chat.id, message_text + 'Введи номер запроса')


@dp.message_handler(state=DeleteSearchRequestState.select_request)
async def get_text(message: Message, state: FSMContext):
    delete_search_request(message.text)

    await state.finish()
