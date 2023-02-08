from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def my_search_terms_markup(search_all: list) -> InlineKeyboardMarkup:
    search_all_markup = InlineKeyboardMarkup(row_width=2)
    for search in search_all:
        search_all_markup.insert(InlineKeyboardButton(text=search.title, callback_data=f'search_menu_{search.title}'))
    return search_all_markup


def search_markup(search: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text='Информация', callback_data=f'search_info_{search}'))
    markup.insert(InlineKeyboardButton(text='Изменить', callback_data=f'search_edit_{search}'))
    markup.insert(InlineKeyboardButton(text='Искать', callback_data=f'search_search_{search}'))
    markup.insert(InlineKeyboardButton(text='Удалить', callback_data=f'search_delete_{search}'))
    markup.add(InlineKeyboardButton(text='<<< К поискам', callback_data=f'search_back_{search}'))
    return markup


def search_markup_info(search: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='<<< меню поиска', callback_data=f'search_menu_{search}'))
    return markup


def search_markup_delete(search: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text='ДА', callback_data=f'delete_yes_{search}'))
    markup.insert(InlineKeyboardButton(text='НЕТ', callback_data=f'search_menu_{search}'))
    markup.add(InlineKeyboardButton(text='<<< меню поиска', callback_data=f'search_menu_{search}'))
    return markup


def search_markup_edit(search: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text='Название', callback_data=f'edit_title_{search}'))
    markup.insert(InlineKeyboardButton(text='Ключевые слова', callback_data=f'edit_text_{search}'))
    markup.insert(InlineKeyboardButton(text='Минимальная цена', callback_data=f'edit_min_{search}'))
    markup.insert(InlineKeyboardButton(text='Максимальная цена', callback_data=f'edit_max_{search}'))
    markup.add(InlineKeyboardButton(text='<<< меню поиска', callback_data=f'search_menu_{search}'))
    return markup
