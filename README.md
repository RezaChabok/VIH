# SecurityFeedBot 🤖

An automated security content aggregator that collects tweets and Medium
posts about cybersecurity topics and sends them to a Telegram channel.

## ✨ Features

- Searches Twitter and Medium for relevant security content.
- Avoids duplicate posts by tracking sent items in a SQLite database.
- Sends notifications via Telegram bots.
- Fully configurable via environment variables.

## 🔧 Setup

1. Clone the repo.
2. Copy `.env.example` to `.env` and fill in your tokens.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`

## 📄 License
MIT
