# VIH - Vulnerability Intelligence Hub

An automated OSINT bot that collects security-related tweets and Medium
articles, stores them in a PostgreSQL database to avoid duplicates, and
sends fresh findings directly to your Telegram channel. Designed for
pentesters, bug bounty hunters, and AppSec engineers who want to stay on
top of the latest threats, write-ups, and CVE announcements with zero
manual effort.

## ✨ Features

- **Multi-source collection** – Twitter (via RapidAPI) and Medium (via
  HTML scraping)
- **Smart deduplication** – SQLAlchemy + PostgreSQL ensure you never see
  the same item twice
- **Telegram notifications** – Two separate bots can deliver content to
  your channel immediately after discovery
- **Fully automated** – GitHub Actions CI/CD pipeline runs the bot every
  day at 6:00 UTC (9:30 AM Iran time)
- **Easy local development** – Docker Compose spins up a PostgreSQL
  instance alongside the bot

## 🧱 Project Structure

```
VIH/
├── main.py                    # Entry point – orchestrates all scrapers
├── config.py                  # Loads environment variables
├── database.py                # SQLAlchemy models and session factory
├── models.py                  # Database schema
├── scrapers/
│   ├── twitter_scraper.py
│   └── medium_scraper.py
├── bot/
│   └── telegram_bot.py        # Synchronous Telegram Bot wrapper
├── docker-compose.yml         # PostgreSQL + bot for local runs
├── Dockerfile
├── requirements.txt
├── .env.example               # Template for required environment variables
└── .github/workflows/
    └── daily_security_feed.yml
```

## ⚙️ How It Works

1. **Collect** – `main.py` iterates over a list of security keywords
   (e.g., "SQL Injection", "OWASP", "CVE", "bug bounty").
2. **Scrape** – `twitter_scraper.py` calls the RapidAPI Twitter endpoint,
   while `medium_scraper.py` fetches Medium's search page and extracts
   embedded JSON data.
3. **Deduplicate** – Before storing, the bot checks the PostgreSQL
   database. Items that already exist are skipped.
4. **Notify** – New tweets are sent via `TELEGRAM_BOT1_TOKEN`, new Medium
   posts via `TELEGRAM_BOT2_TOKEN`, both to the same chat ID.

## 🔧 Quick Start (Local)

1. **Clone the repository**

   ```bash
   git clone https://github.com/RezaChabok/VIH.git
   cd VIH
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # edit .env with your real tokens (Telegram, RapidAPI, DB password)
   ```

3. **Run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

   The bot will execute once. To run it on a schedule locally, you can
   use `cron`, `systemd timers`, or just rely on GitHub Actions.

## ☁️ Automated Execution (GitHub Actions)

The included workflow `.github/workflows/daily_security_feed.yml` runs
the bot **every day at 6:00 UTC**.

**Before the first run**, add the following secrets to your GitHub
repository (`Settings > Secrets and variables > Actions`):

- `TELEGRAM_BOT1_TOKEN`
- `TELEGRAM_BOT2_TOKEN`
- `TELEGRAM_CHAT_ID`
- `RAPIDAPI_KEY`

The workflow spins up a temporary PostgreSQL service, runs the bot, and
tears everything down when finished.

## 📊 Database Schema (PostgreSQL)

Two main tables keep everything organised:

- **`vulnerability_sources`** – stores the original source URL, title,
  preview, author, publication date, optional CVSS score, and CVE ID.
- **`keyword_matches`** – links each source to the keyword(s) that
  triggered its capture, together with the match location (title, content,
  or tags).

This design makes it easy to later add advanced filtering, dashboards, or
analytics on top of the collected data.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)

---

Built with ❤️ by [Reza Chabok](https://github.com/RezaChabok) – because
staying ahead of attackers requires staying ahead of the news.
