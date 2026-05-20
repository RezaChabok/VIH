import requests
from config import TELEGRAM_BOT1_TOKEN, TELEGRAM_BOT2_TOKEN, TELEGRAM_CHAT_ID

class SecurityBot:
    def __init__(self):
        self.token1 = TELEGRAM_BOT1_TOKEN
        self.token2 = TELEGRAM_BOT2_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID

    def send_message(self, text, bot_number=1):
        """ارسال هماهنگ و ساده با requests"""
        token = self.token1 if bot_number == 1 else self.token2
        if not token:
            print(f"Bot {bot_number} token not set.")
            return
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'disable_web_page_preview': True
        }
        try:
            response = requests.post(url, data=payload, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message via bot {bot_number}: {e}")
