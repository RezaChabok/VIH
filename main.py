import time
import datetime
from bot.telegram_bot import SecurityBot
from scrapers.twitter_scraper import TwitterScraper
from scrapers.medium_scraper import MediumScraper

def main():
    bot = SecurityBot()
    twitter = TwitterScraper()
    medium = MediumScraper()

    keywords = ['web penetration testing', 'injection', 'Cross Site Scripting', 'SQL Injection', 'Cross Site Request Forgery', 'Denial of Service', 'Buffer Overflow', 'zero day', 'web security standards', 'web security controls', 'web s>
   'تست نفوذ وب', 'اینجکشن', 'اینجکشن SQL', 'CSRF', 'رایت اپ', 'باگ', 'SQLi', 'bug','Mass Assignment', 'cache deception', 'Subdomain Discovery', 'Asset discovery', 'Service discovery', 'DNS brute force', 'Reverse whois', 'Reverse lookup>
]


    for keyword in keywords:
        print(f"Processing: {keyword}")
        twitter.process(keyword, bot)
        time.sleep(1)

        medium.fetch_and_process(keyword, bot)
        time.sleep(2)

    bot.send_message(f"Daily security feed completed at {datetime.datetime.now()}")

if __name__ == "__main__":
    main()
