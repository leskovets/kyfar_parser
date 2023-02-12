from database.db_hendler import get_search_request
from parsing import kyfar
from database import db_hendler
from loader import dp, logger
from aiogram.utils.markdown import hlink
import asyncio


async def search_all() -> None:

    while True:
        await asyncio.sleep(60*5)
        logger.info("выполняется проверка")
        all_search_response = get_search_request()

        for search_response in all_search_response:
            text = search_response.search_text
            price_min = search_response.price_min
            price_mxa = search_response.price_max
            chat_id = search_response.chat_id

            for advertisement in kyfar.get_advertisements(text=text, price_min=price_min, price_max=price_mxa):
                if not db_hendler.check_advertisement(chat_id=chat_id, advertisement_id=advertisement['id']):
                    text = hlink(advertisement['title'], advertisement['linc'])
                    text += ' Цена: '
                    text += str(advertisement['price']) if not advertisement['price'] == 0 else 'Договорная'
                    await dp.bot.send_message(chat_id, text, parse_mode='HTML')
                    db_hendler.add_advertisement(chat_id=chat_id,
                                                 advertisement_id=advertisement['id'],
                                                 price=advertisement['price'],
                                                 title=advertisement['title'],
                                                 search=search_response)

