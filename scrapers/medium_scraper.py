import requests
from bs4 import BeautifulSoup
import json
from database import get_session, Post
from config import RAPIDAPI_KEY

class MediumScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.base_url = 'https://medium.com/search?q='

    def fetch_and_process(self, keyword, bot):
        session = get_session()
        url = f"{self.base_url}{keyword}"
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Medium for '{keyword}': {e}")
            session.close()
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        scripts = soup.find_all('script')
        data = None
        for script in scripts:
            if script.string and script.string.strip().startswith('window.__APOLLO_STATE__'):
                json_str = script.string.strip()[len('window.__APOLLO_STATE__ = '):]
                try:
                    data = json.loads(json_str)
                    break
                except json.JSONDecodeError:
                    continue

        if not data:
            print(f"No JSON data found for keyword '{keyword}'")
            session.close()
            return

        for key, value in data.items():
            if key.startswith('Post:'):
                title = value.get('title')
                medium_url = value.get('mediumUrl')
                if title and medium_url:
                    existing = session.query(Post).filter_by(link=medium_url).first()
                    if not existing:
                        try:
                            bot.send_message(f"{title}\n{medium_url}", bot_number=2)
                            session.add(Post(link=medium_url, title=title))
                            session.commit()
                        except Exception as e:
                            print(f"Failed to send Medium post: {e}")
        session.close()
