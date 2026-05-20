import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT1_TOKEN = os.getenv('TELEGRAM_BOT1_TOKEN')
TELEGRAM_BOT2_TOKEN = os.getenv('TELEGRAM_BOT2_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
