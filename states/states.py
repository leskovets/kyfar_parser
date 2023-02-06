from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateSearchRequestState(StatesGroup):
    text = State()
    price = State()


class DeleteSearchRequestState(StatesGroup):
    select_request = State()
