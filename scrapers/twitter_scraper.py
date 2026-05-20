import requests
from database import get_session, Tweet
from sqlalchemy.exc import SQLAlchemyError
from config import RAPIDAPI_KEY

class TwitterScraper:
    def __init__(self):
        self.api_url = "https://twitter-api45.p.rapidapi.com/search.php"
        self.headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "twitter-api45.p.rapidapi.com"
        }

    def fetch(self, keyword):
        try:
            response = requests.get(
                self.api_url,
                headers=self.headers,
                params={"query": keyword},
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Twitter API error for '{keyword}': {e}")
            return None

    def process(self, keyword, bot):
        session = get_session()
        try:
            data = self.fetch(keyword)
            if not data:
                return

            tweets = self._extract_tweets(data)
            if not tweets:
                print(f"No tweets extracted for '{keyword}'")
                return

            for tweet in tweets:
                tweet_id = tweet.get('tweet_id')
                text = tweet.get('text')
                if not tweet_id or not text:
                    continue

                existing = session.query(Tweet).filter_by(id=tweet_id).first()
                if existing:
                    continue

                link = f"https://x.com/user/status/{tweet_id}"
                bot.send_message(f"New Tweet:\n{text}\n{link}")

                session.add(Tweet(id=tweet_id, text=text))
                session.commit()

        except SQLAlchemyError as e:
            print(f"Database error for keyword '{keyword}': {e}")
            session.rollback()
        except Exception as e:
            print(f"Unexpected error processing '{keyword}': {e}")
            session.rollback()
        finally:
            session.close()

    def _extract_tweets(self, data):

        tweets = []

        if isinstance(data, dict):
            for key in ('results', 'tweets', 'data', 'timeline'):
                items = data.get(key)
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            tid = item.get('tweet_id') or item.get('id') or item.get('id_str')
                            txt = item.get('text') or item.get('full_text') or item.get('content')
                            if tid and txt:
                                tweets.append({'tweet_id': str(tid), 'text': txt})

            if not tweets and 'tweet_id' in data:
                tid = data.get('tweet_id') or data.get('id')
                txt = data.get('text') or data.get('full_text')
                if tid and txt:
                    tweets.append({'tweet_id': str(tid), 'text': txt})

            if not tweets:
                tweets = self._search_tweets_recursive(data)

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    tid = item.get('tweet_id') or item.get('id') or item.get('id_str')
                    txt = item.get('text') or item.get('full_text') or item.get('content')
                    if tid and txt:
                        tweets.append({'tweet_id': str(tid), 'text': txt})

        return tweets

    def _search_tweets_recursive(self, obj, depth=0):
        if depth > 5:
            return []

        results = []
        if isinstance(obj, dict):
            tid = obj.get('tweet_id') or obj.get('id') or obj.get('id_str')
            txt = obj.get('text') or obj.get('full_text')
            if tid and txt:
                results.append({'tweet_id': str(tid), 'text': txt})
            for value in obj.values():
                results.extend(self._search_tweets_recursive(value, depth + 1))
        elif isinstance(obj, list):
            for item in obj:
                results.extend(self._search_tweets_recursive(item, depth + 1))

        return results
