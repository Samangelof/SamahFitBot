import os
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_BOT_USERNAME = os.getenv('TELEGRAM_BOT_USERNAME')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SERVER_IP = os.getenv('SERVER_IP')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]
# ЮKassa
SHOP_ID = os.getenv('SHOP_ID')
SHOP_SECRET_KEY = os.getenv('SHOP_SECRET_KEY')
PAYMENT_AMOUNT = os.getenv('PAYMENT_AMOUNT')

# База данных
DATABASE_PATH = 'bot_database.db'