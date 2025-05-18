from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.settings.config import BOT_TOKEN
from bot.database.database import DatabaseManager


db = DatabaseManager()

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)