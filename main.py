import time
import datetime
import sys
from bot.telegram_bot import SecurityBot
from scrapers.twitter_scraper import TwitterScraper
from scrapers.medium_scraper import MediumScraper

def main():
    bot = SecurityBot()
    twitter = TwitterScraper()
    medium = MediumScraper()

    keywords = [
    'web penetration testing',
    'injection',
    'Cross Site Scripting',
    'SQL Injection',
    'Cross Site Request Forgery',
    'Denial of Service',
    'Buffer Overflow',
    'zero day',
    'web security standards',
    'web security controls',
    'web security awareness',
    'web security training',
    'web security compliance',
    'OWASP',
    'تست نفوذ وب',
    'اینجکشن',
    'اینجکشن SQL',
    'CSRF',
    'رایت اپ',
    'باگ',
    'SQLi',
    'bug',
    'Mass Assignment',
    'cache deception',
    'Subdomain Discovery',
    'Asset discovery',
    'Service discovery',
    'DNS brute force',
    'Reverse whois',
    'Reverse lookup',
    'Host Header Fuzzing',
    'ASN discovery',
    'behind CDN',
    'XSS',
    'http smuggling',
    'writeup',
    'write_up',
    'Wordpress vulnerability',
    'django vulnerability',
    'waf bypass',
    'payload',
    'bunty',
    'information disclosure',
    'Broken Access Control',
    'Insecure Design',
    'Security Misconfiguration',
    'XXE',
    'XML External Entities',
    'Insecure Deserialization',
    'open redirect',
    'CORS Misconfiguration',
    'Cache Poisoning',
    'IDOR',
    'SSTI',
    'RCE',
    'Command injection',
    'server side template injection',
    'remote code execution',
    'verb tampering',
    'Virtual Host Discovery',
    'Resource discovery',
    'CIDR Discovery',
    'hunt methodology',
    'CVE',
    'Improper Token Generation', 
    'Insecure Email Verification', 
    'Weak Password Reset Mechanisms',
    'Insecure Magic Links',
    'Weak Passwords',
    'DOM XSS',
    'Reflected XSS',
    'PII leakage',
    'Insecure Direct Object Refence'
]

    for keyword in keywords:
        print(f"Processing: {keyword}")
        try:
            twitter.process(keyword, bot)
        except Exception as e:
            print(f"Twitter error for '{keyword}': {e}", file=sys.stderr)

        time.sleep(1)

        print(f"Starting Medium for: {keyword}")
        try:
            medium.fetch_and_process(keyword, bot)
        except Exception as e:
            print(f"Medium error for '{keyword}': {e}", file=sys.stderr)
        print(f"Finished Medium for: {keyword}")

        time.sleep(2)

    bot.send_message(f"Daily security feed completed at {datetime.datetime.now()}")
    bot.send_message(f"Daily security feed completed at {datetime.datetime.now()}", 2)

if __name__ == "__main__":
    main()
