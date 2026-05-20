import requests
from bs4 import BeautifulSoup
import json
import sys
from database import get_session, Post
from sqlalchemy.exc import SQLAlchemyError

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
            print(f"MEDIUM NETWORK ERROR for '{keyword}': {e}", file=sys.stderr)
            session.close()
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        data = self._extract_data(soup)

        if not data:
            print(f"MEDIUM PARSE FAILED for '{keyword}': No data structure matched.", file=sys.stderr)
            with open('medium_debug.html', 'w') as f:
                f.write(response.text[:5000])
            print(f"Saved debug HTML to medium_debug.html", file=sys.stderr)
            session.close()
            return

        self._process_posts(data, bot, session)
        session.close()

    def _extract_data(self, soup):
        scripts = soup.find_all('script')
        for script in scripts:
            if not script.string:
                continue
            text = script.string.strip()

            for prefix in ['window.__APOLLO_STATE__ = ', 'window.__PRELOADED_STATE__ = ']:
                if text.startswith(prefix):
                    json_str = text[len(prefix):]
                    try:
                        data = json.loads(json_str)
                        if data:
                            return data
                    except json.JSONDecodeError:
                        continue

            if script.get('type') == 'application/json':
                try:
                    data = json.loads(text)
                    if data:
                        return data
                except json.JSONDecodeError:
                    continue

        jsonld_scripts = soup.find_all('script', type='application/ld+json')
        for script in jsonld_scripts:
            try:
                data = json.loads(script.string)
                return {'jsonld': data}
            except (json.JSONDecodeError, TypeError):
                continue

        return None

    def _process_posts(self, data, bot, session):
        posts = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if key.startswith('Post:'):
                    posts.append(value)
        
        if isinstance(data, dict) and 'jsonld' in data:
            ld = data['jsonld']
            if isinstance(ld, list):
                for item in ld:
                    if isinstance(item, dict) and item.get('@type') in ('Article', 'BlogPosting', 'SocialMediaPosting'):
                        posts.append(item)
            elif isinstance(ld, dict):
                if ld.get('@type') in ('Article', 'BlogPosting', 'SocialMediaPosting'):
                    posts.append(ld)

        for post in posts:
            title = post.get('title') or post.get('name') or post.get('headline')
            if not title:
                continue

            medium_url = post.get('mediumUrl') or post.get('canonicalUrl') or post.get('url')
            if not medium_url:
                post_id = post.get('id') or post.get('identifier')
                if post_id:
                    medium_url = f"https://medium.com/p/{post_id}"
                else:
                    continue

            try:
                existing = session.query(Post).filter_by(link=medium_url).first()
                if not existing:
                    bot.send_message(f"{title}\n{medium_url}", bot_number=2)
                    session.add(Post(link=medium_url, title=title))
                    session.commit()
            except SQLAlchemyError as e:
                print(f"Database error for post '{title}': {e}", file=sys.stderr)
                session.rollback()
            except Exception as e:
                print(f"Unexpected error for post '{title}': {e}", file=sys.stderr)
