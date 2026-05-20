import requests
import xml.etree.ElementTree as ET
import sys
from database import get_session, Post
from sqlalchemy.exc import SQLAlchemyError

class MediumScraper:
    def __init__(self):
        self.base_url = 'https://medium.com/search?q='

    def fetch_and_process(self, keyword, bot):
        session = get_session()
        url = f"{self.base_url}{keyword}"
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"MEDIUM RSS ERROR for '{keyword}': {e}", file=sys.stderr)
            session.close()
            return

        posts = self._parse_rss(response.text)
        if not posts:
            print(f"MEDIUM RSS PARSE FAILED for '{keyword}': No entries found.", file=sys.stderr)
            session.close()
            return

        for post in posts:
            title = post.get('title')
            link = post.get('link')
            if not title or not link:
                continue

            try:
                existing = session.query(Post).filter_by(link=link).first()
                if not existing:
                    bot.send_message(f"{title}\n{link}", bot_number=2)
                    session.add(Post(link=link, title=title))
                    session.commit()
            except SQLAlchemyError as e:
                print(f"Database error for post '{title}': {e}", file=sys.stderr)
                session.rollback()
            except Exception as e:
                print(f"Unexpected error for post '{title}': {e}", file=sys.stderr)
        session.close()

    def _parse_rss(self, xml_content):
        posts = []
        try:
            root = ET.fromstring(xml_content)
            channel = root.find('channel')
            if channel is None:
                return posts
            for item in channel.findall('item'):
                title = item.findtext('title')
                link = item.findtext('link')
                if title and link:
                    posts.append({'title': title, 'link': link})
        except ET.ParseError as e:
            print(f"XML Parse Error: {e}", file=sys.stderr)
        return posts
