import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('search', "Поиск"),
    ('create_search', 'Создать поиск'),
    ('delete_search', 'Удалить поиск'),
    ('my_search', 'Мои поиски')
)
