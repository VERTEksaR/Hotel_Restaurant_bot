import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

DB_PATH = 'history.db'
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("hello_world", "Поздороваться с миром"),
    ("low", "Вывод минимальных показателей"),
    ("high", "Вывод максимальных показателей"),
    ("custom", "Вывод показателей пользовательского диапазона"),
    ("history", "История запросов")
)
