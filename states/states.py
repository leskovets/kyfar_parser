from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateSearchRequestState(StatesGroup):
    title = State()
    text = State()
    min_price = State()
    max_price = State()
    view_result = State()


class DeleteSearchRequestState(StatesGroup):
    select_request = State()


class EditSearchRequestState(StatesGroup):
    title = State()
    text = State()
    min = State()
    max = State()
