# test_webhook.py
import aiohttp
import asyncio
import sqlite3
import hmac
import hashlib
import base64
import json


DATABASE_PATH = 'bot_database.db'
SHOP_SECRET_KEY = ''

def compute_signature(request_body_bytes: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode(), request_body_bytes, hashlib.sha256).digest()
    return base64.b64encode(digest).decode()

async def simulate_payment_notification():
    """
    Имитирует уведомление от ЮKassa о успешной оплате
    """

    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT payment_id FROM applications WHERE payment_status = 'не оплачено' ORDER BY id DESC LIMIT 1"
            )
            result = cursor.fetchone()
            
            if not result or not result[0]:
                print("Не найдено неоплаченных заявок с payment_id")
                return
            
            payment_id = result[0]
            
        test_data = {
            "event": "payment.succeeded",
            "object": {
                "id": "test_payment_" + payment_id[:8],
                "status": "succeeded",
                "amount": {
                    "value": "1590.00",
                    "currency": "RUB"
                },
                "metadata": {
                    "label": payment_id
                }
            }
        }
        # Сериализуем json ТОЛЬКО в байтах!
        raw_data = json.dumps(test_data, ensure_ascii=False, separators=(',', ':')).encode()
        signature = compute_signature(raw_data, SHOP_SECRET_KEY)

        headers = {
            "Content-Type": "application/json",
            "Idempotence-Key": signature
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://.../yookassa-webhook",
                data=raw_data,
                headers=headers
            ) as response:
                status = response.status
                text = await response.text()
                print(f"Статус ответа: {status}")
                print(f"Текст ответа: {text}")
                
                if status == 200:
                    print(f"✅ Тестовое уведомление об оплате успешно обработано для payment_id: {payment_id}")
                else:
                    print(f"❌ Ошибка при обработке тестового уведомления")
    
    except Exception as e:
        print(f"Ошибка при тестировании webhook: {str(e)}")


if __name__ == "__main__":
    asyncio.run(simulate_payment_notification())