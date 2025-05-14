import logging
import asyncio
from aiogram.utils.exceptions import NetworkError
from bot.settings.setup_bot import dp, bot, storage, db
from bot.handlers.controller import register_handlers
from bot.utils.logger import log_info
from bot.payment_api.webhook_server import run_webhook_app
from bot.services.openai_client import openai_client


async def start_polling_with_retry():
    """Запуск polling с повторными попытками при ошибках сети."""
    retry_count = 5
    delay = 5
    for attempt in range(retry_count):
        try:
            await dp.start_polling()
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
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Инициализация
    log_info(f"DB instance: {db}")
    register_handlers(dp)
    
    # Запуск вебхук-сервера как фоновой задачи
    webhook_task = asyncio.create_task(run_webhook_app())

    if not openai_client.session:
        await openai_client._create_session()

    try:
        await start_polling_with_retry()
    except Exception as e:
        log_info(f"Бот остановлен из-за ошибки: {e}")
    finally:
        # Корректное завершение
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
