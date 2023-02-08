from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from keyboards.inline.my_search_murkup import my_search_terms_markup, search_markup, search_markup_info
from keyboards.inline.my_search_murkup import search_markup_delete, search_markup_edit
from loader import dp, bot
from database.db_hendler import get_search_request_user, delete_search_request, get_search_request_user_title
from database.db_hendler import check_search_request_user_title
from parsing import kyfar
from states.states import EditSearchRequestState


@dp.message_handler(commands='my_search')
async def my_search(message: Message):
    my_requests = get_search_request_user(message.chat.id)
    await bot.send_message(message.chat.id, 'Выбери поиск', reply_markup=my_search_terms_markup(my_requests))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('search_menu_'))
async def search_menu(callback: CallbackQuery):
    await callback.answer()
    search_title = callback.data.split('_')[2]
    await bot.edit_message_text('Выбери действие', callback.message.chat.id, callback.message.message_id,
                                reply_markup=search_markup(search_title))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('search_edit_'))
async def search_edit(callback: CallbackQuery):
    await callback.answer()
    search_title = callback.data.split('_')[2]
    await bot.edit_message_text('Что нужно изменить?', callback.message.chat.id, callback.message.message_id,
                                reply_markup=search_markup_edit(search_title))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('edit_'))
async def search_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    command = callback.data.split('_')[1]
    async with state.proxy() as data:
        data['title'] = callback.data.split('_')[2]
    if command == 'title':
        await EditSearchRequestState.title.set()
        await bot.send_message(callback.message.chat.id, "Введи новое название поиска")
    if command == 'text':
        await EditSearchRequestState.text.set()
        await bot.send_message(callback.message.chat.id, "Введи ключевые фразы через запятую")
    if command == 'min':
        await EditSearchRequestState.min.set()
        await bot.send_message(callback.message.chat.id, "Введи минимальную цену")
    if command == 'max':
        await EditSearchRequestState.max.set()
        await bot.send_message(callback.message.chat.id, "Введи максимальную цену")


@dp.message_handler(state=EditSearchRequestState.title)
async def edit_title(message: Message, state: FSMContext):
    try:
        if check_search_request_user_title(message.chat.id, message.text):
            raise TypeError('Такое название уже существует\nПридумайте новое')
    except TypeError as e:
        await bot.send_message(message.chat.id, e)
        return

    await state.finish()


@dp.message_handler(state=EditSearchRequestState.text)
async def edit_title(message: Message, state: FSMContext):
    await state.finish()


@dp.message_handler(state=EditSearchRequestState.min)
async def edit_title(message: Message, state: FSMContext):
    try:
        if not message.text.isdigit():
            raise TypeError('Введи число!')
    except TypeError as e:
        await bot.send_message(message.chat.id, e)
        return
    await state.finish()


@dp.message_handler(state=EditSearchRequestState.max)
async def edit_title(message: Message, state: FSMContext):
    try:
        if not message.text.isdigit():
            raise TypeError('Введи число!')
        with state.proxy() as data:
            search = get_search_request_user_title(message.chat.id, data['title'])
        if int(search.price_range.split(',')[0]) > int(message.text):
            raise TypeError('Введи число больше минимального!')
    except TypeError as e:
        await bot.send_message(message.chat.id, e)
        return
    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('search_delete_'))
async def search_delete(callback: CallbackQuery):
    await callback.answer('Запрос удалён!')
    await bot.edit_message_text('удалить выбранный поиск?', callback.message.chat.id, callback.message.message_id,
                                reply_markup=search_markup_delete(callback.data.split('_')[2]))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete_yes_'))
async def search_delete_yes_no(callback: CallbackQuery):
    await callback.answer('Запрос удалён!')
    delete_search_request(callback.data.split('_')[2])
    my_requests = get_search_request_user(callback.message.chat.id)
    await bot.edit_message_text('Выбери поиск', callback.message.chat.id, callback.message.message_id,
                                reply_markup=my_search_terms_markup(my_requests))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('search_search_'))
async def search_delete(callback: CallbackQuery):
    search = get_search_request_user_title(callback.message.chat.id, callback.data.split('_')[2])
    await callback.answer()
    for advertisement in kyfar.get_advertisements(text=search.search_text, price_range=search.price_range):
        text = hlink(advertisement['title'], advertisement['linc'])
        text += ' Цена: '
        text += str(advertisement['price']) if not advertisement['price'] == 0 else 'Договорная'
        await dp.bot.send_message(callback.message.chat.id, text, parse_mode='HTML')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('search_back_'))
async def search_delete(callback: CallbackQuery):
    my_requests = get_search_request_user(callback.message.chat.id)
    await bot.edit_message_text('Выбери поиск', callback.message.chat.id, callback.message.message_id,
                                reply_markup=my_search_terms_markup(my_requests))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('search_info_'))
async def search_info(callback: CallbackQuery):
    await callback.answer()
    search = get_search_request_user_title(callback.message.chat.id, callback.data.split('_')[2])
    text = f'Название: {search.title}\n' \
           f'Запросы: {search.search_text}\n' \
           f'Мин цена: {search.price_range.split(",")[0]} Макс. цена: {search.price_range.split(",")[1]}\n'

    await bot.edit_message_text(text, callback.message.chat.id, callback.message.message_id,
                                reply_markup=search_markup_info(callback.data.split('_')[2]))
