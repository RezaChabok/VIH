import requests
import re
from config import RAPIDAPI_KEY
from database import get_session, Tweet

class TwitterScraper:
    def __init__(self):
        self.api_url = "https://twitter-api45.p.rapidapi.com/search.php"
        self.headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "twitter-api45.p.rapidapi.com"
        }

    def fetch(self, keyword):
        response = requests.get(self.api_url, headers=self.headers, params={"query": keyword})
        return response.json()

    def process(self, keyword, bot):
        session = get_session()
        data = self.fetch(keyword)
        tweets = re.findall(r"'tweet_id': '(.+?)', .+?, 'text': '(.+?)', .+?}", str(data), re.DOTALL)
        for tweet_id, text in tweets:
            if not session.query(Tweet).filter_by(id=tweet_id).first():
                link = f"https://x.com/user/status/{tweet_id}"
                asyncio.run(bot.send_message(f"New Tweet:\n{text}\n{link}"))
                session.add(Tweet(id=tweet_id, text=text))
                session.commit()
        session.close()
