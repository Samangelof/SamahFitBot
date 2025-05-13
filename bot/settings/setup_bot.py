from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.settings.config import BOT_TOKEN, DATABASE_PATH
from bot.database.sqlite_db import DatabaseManager


db = DatabaseManager(DATABASE_PATH)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)