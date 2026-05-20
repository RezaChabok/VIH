import asyncio
from telegram import Bot
from config import TELEGRAM_BOT1_TOKEN, TELEGRAM_BOT2_TOKEN, TELEGRAM_CHAT_ID

class SecurityBot:
    def __init__(self):
        self.bot1 = Bot(token=TELEGRAM_BOT1_TOKEN) if TELEGRAM_BOT1_TOKEN else None
        self.bot2 = Bot(token=TELEGRAM_BOT2_TOKEN) if TELEGRAM_BOT2_TOKEN else None
        self.chat_id = TELEGRAM_CHAT_ID

    async def send_message(self, text, bot_number=1):
        bot = self.bot1 if bot_number == 1 else self.bot2
        if bot:
            try:
                await bot.send_message(chat_id=self.chat_id, text=text)
            except Exception as e:
                print(f"Failed to send message: {e}")
