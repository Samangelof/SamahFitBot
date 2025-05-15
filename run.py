import logging
import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.exceptions import NetworkError

from bot.settings.config import TELEGRAM_BOT_TOKEN
from bot.database.session import init_db, SessionLocal
from bot.handlers.controller import register_handlers
from bot.utils.logger import log_info
from bot.payment_api.webhook_server import run_webhook_app
from bot.services.openai_client import openai_client

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Инициализация базы данных
init_db()

# Middleware для SQLAlchemy-сессии
@dp.middleware()
async def db_session_middleware(handler, event, data):
    db = SessionLocal()
    try:
        data["db"] = db
        return await handler(event, data)
    finally:
        db.close()

# Регистрация хендлеров
register_handlers(dp)

async def start_polling_with_retry():
    retry_count = 5
    delay = 5
    for attempt in range(retry_count):
        try:
            await dp.start_polling(bot)
            break
        except NetworkError as e:
            log_info(f"Ошибка сети ({e}): попытка {attempt + 1} из {retry_count}.")
            if attempt < retry_count - 1:
                await asyncio.sleep(delay)
            else:
                log_info("Не удалось подключиться к Telegram API после нескольких попыток.")
                raise
        except Exception as e:
            log_info(f"Неизвестная ошибка при запуске бота: {e}")
            raise

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    log_info("Бот запускается...")

    # Запуск вебхука
    webhook_task = asyncio.create_task(run_webhook_app())

    if not openai_client.session:
        await openai_client._create_session()

    try:
        await start_polling_with_retry()
    except Exception as e:
        log_info(f"Бот остановлен из-за ошибки: {e}")
    finally:
        await openai_client.close_session()
        webhook_task.cancel()
        try:
            await webhook_task
        except asyncio.CancelledError:
            pass

        await storage.close()
        await storage.wait_closed()
        await bot.close()
        log_info("Все ресурсы освобождены")

if __name__ == "__main__":
    asyncio.run(main())
