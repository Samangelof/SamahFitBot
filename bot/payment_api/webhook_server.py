# webhook_server.py
from aiohttp import web
import sqlite3
import json
from bot.settings.config import DATABASE_PATH, ADMIN_CHAT_ID, BOT_TOKEN, SHOP_SECRET_KEY
from aiogram import Bot
from bot.utils.logger import log_info
from bot.services.payment_service import send_thank_you_message
from bot.utils.utils import format_application
from bot.settings.setup_bot import db


import hashlib
import hmac
import base64


bot = Bot(token=BOT_TOKEN)

async def handle_webhook(request):
    try:
        raw_data = await request.read()
        data = await request.json()
        
        signature = (
            request.headers.get('X-Webhook-Signature-SHA256') or
            request.headers.get('Idempotence-Key')
        )

        
        shop_secret = SHOP_SECRET_KEY
        if not verify_signature(raw_data, signature, shop_secret):
            log_info("Неверная подпись вебхука")
            return web.Response(status=401, text="Неверная подпись")
        
        payment_id = data.get("object", {}).get("id", "unknown")
        label = data.get("object", {}).get("metadata", {}).get("label")
        notification_type = data.get("event")
        amount = data.get("object", {}).get("amount", {}).get("value")
        status = data.get("object", {}).get("status")
        
        log_info(f"Webhook получен: {notification_type}, label: {label}, payment_id: {payment_id}, status: {status}")

        if notification_type != "payment.succeeded" or status != "succeeded":
            return web.Response(text="Ignored: Not a successful payment event")

        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                """UPDATE applications 
                SET payment_status = ?, 
                    payment_date = CURRENT_TIMESTAMP 
                WHERE payment_id = ?""",
                ('оплачено', label)
            )
            
            if cursor.rowcount == 0:
                log_info(f"Заявка с payment_id: {label} не найдена")
                return web.Response(text="Application not found")

            cursor.execute('''
                SELECT u.telegram_id, u.first_name, u.username, a.answers, a.id as application_id
                FROM applications a
                JOIN users u ON a.user_id = u.id
                WHERE a.payment_id = ?
            ''', (label,))
            
            row = cursor.fetchone()
            if not row:
                log_info(f"Не удалось получить данные пользователя для payment_id: {label}")
                return web.Response(text="User data not found")
            
            user_telegram_id = row['telegram_id']
            user_first_name = row['first_name']
            user_username = row['username']
            application_id = row['application_id']
            log_info(f"answers from DB: {row['answers']}")
            answers = json.loads(row['answers'])
            conn.commit()

            # <<< ВСТАВЬ ЭТО СЮДА >>>
            db.mark_referral_paid(user_telegram_id)
            # <<< ВСТАВЬ ЭТО СЮДА >>>

            
            await send_thank_you_message(user_telegram_id)

            message = format_application(answers, user_first_name, user_username, application_id, amount)

            try:
                await bot.send_message(ADMIN_CHAT_ID, message, parse_mode="HTML")
                log_info(f"Уведомление отправлено админу о платеже для заявки {application_id}")
            except Exception as e:
                log_info(f"Ошибка отправки сообщения админу: {str(e)}")

        return web.Response(text="OK")

    except json.JSONDecodeError:
        log_info("Ошибка декодирования JSON в запросе")
        return web.Response(status=400, text="Некорректный JSON")
    except Exception as e:
        log_info(f"Ошибка обработки webhook: {str(e)}")
        return web.Response(status=500, text="Внутренняя ошибка сервера")

def verify_signature(raw_data, signature, secret_key):
    """Проверка подписи от ЮKassa"""
    if not signature:
        return False
    
    computed_signature = hmac.new(
        secret_key.encode(),
        raw_data,
        hashlib.sha256
    ).digest()
    
    computed_signature_b64 = base64.b64encode(computed_signature).decode()
    
    return hmac.compare_digest(computed_signature_b64, signature)

async def run_webhook_app():
    app = web.Application()
    app.router.add_post("/yookassa-webhook", handle_webhook)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    try:
        site = web.TCPSite(runner, host='0.0.0.0', port=8443)
        await site.start()
        log_info("Webhook сервер запущен на порту 8443")
        return runner
    except Exception as e:
        log_info(f"Не удалось запустить webhook сервер: {str(e)}")
        await runner.cleanup()
        raise