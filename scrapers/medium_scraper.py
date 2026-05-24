import requests
import sys
from database import get_session, Post
from sqlalchemy.exc import SQLAlchemyError
from config import RAPIDAPI_KEY_MEDIUM

class MediumScraper:
    def __init__(self):
        self.api_url = "https://medium2.p.rapidapi.com/search/articles"
        self.headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY_MEDIUM,
            "X-RapidAPI-Host": "medium2.p.rapidapi.com",
            "Content-Type": "application/json"
        }

    def fetch_and_process(self, keyword, bot):
        session = get_session()
        posts = self._fetch_posts(keyword)

        if posts is None:
            print(f"RapidAPI failed for '{keyword}' – skipping.", file=sys.stderr)
            session.close()
            return

        for post in posts:
            title = post.get('title')
            link = post.get('url')
            if not title or not link:
                continue

            try:
                existing = session.query(Post).filter_by(link=link).first()
                if not existing:
                    bot.send_message(f"{title}\n{link}", bot_number=2)
                    session.add(Post(link=link, title=title))
                    session.commit()
            except SQLAlchemyError as e:
                print(f"DB error for '{title}': {e}", file=sys.stderr)
                session.rollback()
            except Exception as e:
                print(f"Send error for '{title}': {e}", file=sys.stderr)

        session.close()

    def _fetch_posts(self, keyword):
        try:
            params = {"q": keyword, "limit": 10}
            resp = requests.get(self.api_url, headers=self.headers, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"RapidAPI request error: {e}", file=sys.stderr)
            return None

        return self._extract_posts(data)

    def _extract_posts(self, data):
        candidates = []
        if isinstance(data, list):
            candidates = data
        elif isinstance(data, dict):
            for key in ('articles', 'items', 'data', 'results', 'posts'):
                items = data.get(key)
                if isinstance(items, list):
                    candidates = items
                    break
            if not candidates and 'title' in data:
                candidates = [data]

        posts = []
        for item in candidates:
            if not isinstance(item, dict):
                continue
            title = item.get('title') or item.get('name')
            link = item.get('url') or item.get('link') or item.get('mediumUrl')
            if title and link:
                posts.append({'title': title, 'url': link})
        return posts