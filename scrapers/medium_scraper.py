import requests
import sys
import time
from database import get_session, Post
from sqlalchemy.exc import SQLAlchemyError
from config import RAPIDAPI_KEY_MEDIUM

class MediumScraper:
    def __init__(self):
        self.base_url = "https://medium2.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": RAPIDAPI_KEY_MEDIUM,
            "x-rapidapi-host": "medium2.p.rapidapi.com"
        }

    def fetch_and_process(self, keyword, bot):
        session = get_session()
        article_ids = self._search_articles(keyword)
        if not article_ids:
            print(f"No articles found for '{keyword}'", file=sys.stderr)
            session.close()
            return

        for article_id in article_ids[:5]:
            post = self._get_article_info(article_id)
            if not post:
                continue
            
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
            
            time.sleep(1)

        session.close()

    def _search_articles(self, query):
        try:
            resp = requests.get(
                f"{self.base_url}/search/articles",
                headers=self.headers,
                params={"query": query},
                timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
            
            if isinstance(data, dict) and 'articles' in data:
                return data['articles']
            elif isinstance(data, list):
                return data
            else:
                print(f"Unexpected search response: {data}", file=sys.stderr)
                return []
        except Exception as e:
            print(f"Search error for '{query}': {e}", file=sys.stderr)
        return []

    def _get_article_info(self, article_id):
        try:
            resp = requests.get(
                f"{self.base_url}/article/{article_id}",
                headers=self.headers,
                timeout=15
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Article info error for {article_id}: {e}", file=sys.stderr)
        return None
