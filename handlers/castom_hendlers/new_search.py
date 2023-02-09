from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from database import db_hendler
from keyboards.reply.new_search_markup import keyboard_old_new
from parsing import kyfar
from states.states import CreateSearchRequestState
from loader import dp, bot
from database.db_hendler import add_search_request, get_search_text_request
from database.db_hendler import get_search_request_user, check_search_request_user_title


@dp.message_handler(commands='new_search')
async def create_search_request(message: Message):
    try:
        if len(get_search_request_user(message.chat.id)) == 4:
            raise TypeError('Вы уже создали максимальное количество поисков на бесплатном аккаунте!')
    except TypeError as e:
        await bot.send_message(message.chat.id, e)
        return
    await CreateSearchRequestState.title.set()
    await bot.send_message(message.chat.id, 'Придумай название для поиска')


@dp.message_handler(state=CreateSearchRequestState.title)
async def get_text(message: Message, state: FSMContext):
    try:
        if check_search_request_user_title(message.chat.id, message.text):
            raise TypeError('Такое название уже существует\nПридумайте новое или измените поиск с этим названием')
    except TypeError as e:
        await bot.send_message(message.chat.id, e)
        return
    async with state.proxy() as data:
        data['title'] = message.text

    await CreateSearchRequestState.next()
    await bot.send_message(message.chat.id, 'Введи ключевые фразы для поиска через запятую')


@dp.message_handler(state=CreateSearchRequestState.text)
async def get_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['search_text'] = message.text

    await CreateSearchRequestState.next()
    await bot.send_message(message.chat.id, 'Введи минимальную цену, чтобы отсеять всякие аксессуары')


@dp.message_handler(state=CreateSearchRequestState.min_price)
async def get_min_price(message: Message, state: FSMContext):
    try:
        if not message.text.isdigit():
            raise TypeError('Введи число!')
    except TypeError as e:
        await bot.send_message(message.chat.id, e)
        return
    async with state.proxy() as data:
        data['min_price'] = message.text

    await CreateSearchRequestState.next()
    await bot.send_message(message.chat.id, 'Введи максимальную цену за которую готов купить.')


@dp.message_handler(state=CreateSearchRequestState.max_price)
async def get_max_price(message: Message, state: FSMContext):
    try:
        if not message.text.isdigit():
            raise TypeError('Введи число!')
        async with state.proxy() as data:
            if int(data['min_price']) > int(message.text):
                raise TypeError('Введи число больше минимального!')
    except TypeError as e:
        await bot.send_message(message.chat.id, e)
        return

    async with state.proxy() as data:
        data['max_price'] = message.text
    await CreateSearchRequestState.next()
    await bot.send_message(message.chat.id, 'Вывести результаты уже существующих предложений или только новых?',
                           reply_markup=keyboard_old_new)


@dp.message_handler(state=CreateSearchRequestState.view_result)
async def create_search_request(message: Message, state: FSMContext):

    try:
        if not (message.text == 'Существ.' or message.text == 'Новые'):
            raise TypeError('Выбери из предложенных вариантов!',
                            reply_markup=keyboard_old_new)
    except TypeError as e:
        await dp.bot.send_message(message.chat.id, e)
        return

    async with state.proxy() as data:
        title = data['title']
        search_text = data['search_text']
        price_min = data['min_price']
        price_max = data['max_price']

    add_search_request(chat_id=message.chat.id, title=title, search_text=search_text,
                       price_min=price_min, price_max=price_max)

    await state.finish()
    await bot.send_message(message.chat.id, 'Поиск создан!', reply_markup=ReplyKeyboardRemove())

    search = get_search_text_request(search_text)
    kyfar_response = kyfar.get_advertisements(text=search_text, price_min=price_min, price_max=price_max)
    for advertisement in kyfar_response:
        db_hendler.add_advertisement(chat_id=message.chat.id,
                                     advertisement_id=advertisement['id'],
                                     price=advertisement['price'],
                                     title=advertisement['title'],
                                     search=search)
        if message.text == 'Существ.':
            text = hlink(advertisement['title'], advertisement['linc'])
            text += ' Цена: '
            text += str(advertisement['price']) if not advertisement['price'] == 0 else 'Договорная'
            await dp.bot.send_message(message.chat.id, text, parse_mode='HTML')
