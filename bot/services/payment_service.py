# payment_utils.py
import uuid
import aiohttp
import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.logger import log_info
from bot.settings.config import SHOP_ID, SHOP_SECRET_KEY, PAYMENT_AMOUNT, TELEGRAM_BOT_USERNAME
import base64



async def check_payment_status(payment_id: str) -> bool:
    """
    Проверка статуса платежа через API ЮKassa.
    Возвращает True, если платеж был успешно завершен, иначе False.
    """
    auth_string = f"{SHOP_ID}:{SHOP_SECRET_KEY}"
    basic_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {basic_auth}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.yookassa.ru/v3/payments/{payment_id}",
                headers=headers
            ) as response:
                if response.status == 200:
                    response_data = await response.json()
                    payment_status = response_data.get('status')
                    if payment_status == 'succeeded':
                        return True
                return False
    except Exception as e:
        log_info(f"Ошибка при проверке статуса платежа: {str(e)}", exc_info=True)
        return False


async def handle_payment_reminder(message, payment_id: str, confirmation_url: str):
    """
    Напоминание пользователю о необходимости оплаты через 24 часа,
    если платеж не был завершен.
    """
    await asyncio.sleep(86400)

    if not await check_payment_status(payment_id):
        await message.answer(
            "Ты ещё не оплатил. Пожалуйста, перейди по ссылке для завершения оплаты.",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("Оплатить", url=confirmation_url)
            )
        )
        log_info(f"Отправлено напоминание о платеже для payment_id: {payment_id}")

async def generate_payment_link(message: types.Message, state: FSMContext, application_id: int):
    """
    Генерирует ссылку на оплату через ЮKassa
    """
    from bot.database.sqlite_db import DatabaseManager
    from bot.settings.config import DATABASE_PATH
    
    db = DatabaseManager(DATABASE_PATH)
    
    # 1. Получаем Telegram ID пользователя
    telegram_id = message.from_user.id

    # 2. Считаем скидку
    discount_percent = db.get_discount_percent(telegram_id)
    
    # 3. Считаем финальную сумму
    base_amount = float(PAYMENT_AMOUNT)  # например 1590₽
    final_amount = base_amount * (1 - discount_percent / 100)
    final_amount = round(final_amount, 2)  # округляем до копеек, как требует ЮKassa
    
    payment_id = str(uuid.uuid4())
    db.update_payment_status(application_id, "не оплачено", payment_id)

    
    payment_data = {
        "amount": {
            "value": str(final_amount),
            "currency": "RUB"
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/{TELEGRAM_BOT_USERNAME}"
        },
        "description": f"Оплата персональной программы. Заявка #{application_id}",
        "metadata": {
            "label": payment_id
        }
    }
    auth_string = f"{SHOP_ID}:{SHOP_SECRET_KEY}"
    basic_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Content-Type": "application/json",
        "Idempotence-Key": payment_id,
        "Authorization": f"Basic {basic_auth}"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.yookassa.ru/v3/payments",
                json=payment_data,
                headers=headers
            ) as response:
                if response.status == 200:
                    response_data = await response.json()
                    confirmation_url = response_data.get('confirmation', {}).get('confirmation_url')
                    
                    if confirmation_url:
                        await message.answer(
                            "Для получения персональной программы необходимо произвести оплату.\n\n"
                            f"Сумма к оплате с учётом скидки: {final_amount} руб. (скидка {discount_percent}%)\n\n"
                            "Нажмите на кнопку ниже для перехода к оплате:",
                            reply_markup=types.InlineKeyboardMarkup().add(
                                types.InlineKeyboardButton("Оплатить", url=confirmation_url)
                            )
                        )
                        asyncio.create_task(handle_payment_reminder(message, payment_id, confirmation_url))
                        log_info(f"Создана ссылка на оплату для заявки {application_id}, payment_id: {payment_id}")
                        return True
                    else:
                        log_info(f"Ошибка при создании платежа: отсутствует confirmation_url в ответе")
                else:
                    error_data = await response.text()
                    log_info(f"Ошибка при создании платежа: {response.status} - {error_data}")
        
        await message.answer(
            "Извини, произошла ошибка при создании платежа. Пожалуйста, попробуй позже или свяжись с администратором."
        )
        return False
        
    except Exception as e:
        log_info(f"Исключение при создании платежа: {str(e)}", exc_info=True)
        await message.answer(
            "Извини, произошла ошибка при создании платежа. Пожалуйста, попробуй позже или свяжись с администратором."
        )
        return False


async def send_thank_you_message(user_id: int):
    """
    Отправка благодарственного сообщения после успешной оплаты
    """
    from aiogram import Bot
    from settings.config import BOT_TOKEN
    
    bot = Bot(token=BOT_TOKEN)
    
    try:
        await bot.send_message(
            user_id,
            "Спасибо за оплату!\n"
            "Ты сделал(а) первый шаг к своей новой форме!\n"
            "Готовимся менять жизнь!\n\n"
            "⚙️ Сейчас я анализирую твои ответы и подбираю персональную программу тренировок и питания.\n"
            "Все делаю вручную, с душой и вниманием к деталям — никакого копипаста!\n\n"
            "⏳ Ожидай PDF-документ в течение 1–2 рабочих дней — там будет всё:\n"
            "что есть 🍽️, как тренироваться 🏋️‍♀️, когда отдыхать 💤 и как уверенно идти к цели!\n\n"
            "Если что-то захочешь уточнить — пиши, я всегда на связи!\n\n"
            "Скоро начнём!\n"
            "🔥 #ТвойПутьНачался"
        )
        log_info(f"Отправлено благодарственное сообщение пользователю {user_id}")
        return True
    except Exception as e:
        log_info(f"Ошибка при отправке благодарственного сообщения: {str(e)}", exc_info=True)
        return False