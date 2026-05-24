# VIH - Vulnerability Intelligence Hub

An automated OSINT bot that collects security-related tweets and Medium
articles, stores them in a persistent SQLite database to avoid duplicates,
and delivers fresh findings directly to your Telegram channel via two
specialized bots. Fully automated with **GitHub Actions** and designed as a
central **hub** for your daily vulnerability intelligence.

## ✨ Features

- **Multi‑source collection** – Twitter (via RapidAPI) and Medium (via
  RapidAPI article search + info endpoints)
- **Smart deduplication** – SQLAlchemy + SQLite with a **persistent cache**
  between workflow runs, so you never see the same item twice
- **Dual Telegram bots** – One bot for Twitter, another for Medium, both
  sending to the same chat
- **Fully automated** – GitHub Actions CI/CD pipeline runs the hub **every
  day at 6:00 UTC** (9:30 AM Iran time)
- **Resilient architecture** – Multi‑method extraction for Twitter, two‑step
  lookup for Medium, automatic fallbacks, and comprehensive error handling
- **Easy local development** – Docker Compose for a quick start, or run
  directly with Python

## 🧱 Project Structure

```
VIH/
├── main.py                    # Entry point – orchestrates all scrapers
├── config.py                  # Loads environment variables via decouple
├── database.py                # SQLAlchemy models and session factory
├── scrapers/
│   ├── twitter_scraper.py     # Twitter API via RapidAPI
│   └── medium_scraper.py      # Medium search + article info via RapidAPI
├── bot/
│   └── telegram_bot.py        # Synchronous Telegram Bot (requests‑based)
├── docker-compose.yml         # For local runs
├── Dockerfile
├── requirements.txt
├── .env.example               # Template for required environment variables
└── .github/workflows/
    └── daily_security_feed.yml
```

## ⚙️ How It Works

1. **Collect** – `main.py` iterates over a curated list of security keywords
   (e.g., "SQL Injection", "OWASP", "CVE", "bug bounty").
2. **Scrape** –
   * `twitter_scraper.py` calls the RapidAPI Twitter endpoint and
     parses the JSON response with multi‑key extraction.
   * `medium_scraper.py` first searches for article IDs, then fetches
     full article details (title + URL) for each ID.
3. **Deduplicate** – Before storing, the hub checks the SQLite database.
   Items that already exist are skipped. The database file (`vih.db`)
   is **persisted across runs** via GitHub Actions Cache.
4. **Notify** – New tweets are sent via `TELEGRAM_BOT1_TOKEN`, new Medium
   posts via `TELEGRAM_BOT2_TOKEN`, both to the same chat ID.

## 🛠️ Tech Stack

- **Runtime:** Python 3.10+
- **HTTP:** `requests`
- **Database:** SQLAlchemy + SQLite
- **Telegram:** `requests`‑based synchronous bot (no async overhead)
- **Configuration:** `python-decouple` (secrets never committed)
- **CI/CD:** GitHub Actions with scheduled daily runs
- **Local dev:** Docker Compose

## 🔧 Quick Start (Local)

1. **Clone the repository**

   ```bash
   git clone https://github.com/RezaChabok/VIH.git
   cd VIH
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your real tokens (Telegram, RapidAPI)
   ```

3. **Run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

   Or run directly:

   ```bash
   pip install -r requirements.txt
   python main.py
   ```

   The hub will execute once. For local scheduling, use `cron` or
   `systemd timers`.

## ☁️ Automated Execution (GitHub Actions)

The workflow `.github/workflows/daily_security_feed.yml` runs the hub
**every day at 6:00 UTC**.

**Before the first run**, add these secrets to your GitHub repository
(`Settings > Secrets and variables > Actions`):

| Secret Name              | Description                                      |
|--------------------------|--------------------------------------------------|
| `TELEGRAM_BOT1_TOKEN`    | Token of the first Telegram bot (Twitter feed)   |
| `TELEGRAM_BOT2_TOKEN`    | Token of the second Telegram bot (Medium feed)   |
| `TELEGRAM_CHAT_ID`       | Numerical chat ID to send messages to            |
| `RAPIDAPI_KEY`           | RapidAPI key for Twitter API                     |
| `RAPIDAPI_KEY_MEDIUM`    | RapidAPI key for Medium API                      |

The workflow also uses **GitHub Actions Cache** to persist the SQLite
database (`vih.db`) between runs, ensuring deduplication works across
days.

## 📊 Database Schema (SQLite)

Two tables keep the hub's memory:

| Table     | Primary Key       | Fields                        | Purpose                         |
|-----------|-------------------|-------------------------------|---------------------------------|
| `tweets`  | `id` (BigInteger) | `id`, `text`                  | Stores seen tweet IDs and text  |
| `posts`   | `link` (String)   | `link`, `title`               | Stores seen Medium article URLs |

## 🧪 Resilience Features

- **Twitter:** Structured JSON parsing with multiple possible key names
  (`tweet_id`, `id_str`, `full_text`, etc.) plus recursive search as
  a last resort.
- **Medium:** Two‑step RapidAPI flow (search → article info) completely
  bypasses Cloudflare and RSS parsing issues.
- **Database:** SQLite is lightweight and fast; persistent cache in GitHub
  Actions means no data loss between runs.
- **Error handling:** Every scraper and database operation is wrapped in
  try/except, so a single failure never stops the whole hub.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)

---

Built with ❤️ by [Reza Chabok](https://github.com/RezaChabok) – because
staying ahead of attackers requires your own intelligence hub.
