from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_new = KeyboardButton('Новые')
button_old = KeyboardButton('Существ.')

keyboard_old_new = ReplyKeyboardMarkup(resize_keyboard=True).row(button_new, button_old)
