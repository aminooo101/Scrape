cat > job-scraper/README.md << 'EOF'
# Job Scraper — Python Automated Job Alerts

> Scrapes 4 remote job boards daily, filters by keywords and seniority level, and sends email alerts with new listings.

![Python](https://img.shields.io/badge/python-3.12-blue)
![Sources](https://img.shields.io/badge/sources-4%20job%20boards-teal)
![Email](https://img.shields.io/badge/alerts-email-green)

## What it does

Monitors RemoteOK, Remotive, Arbeitnow, and Himalayas every day at 9am. Filters out senior roles automatically. Sends an email only when new junior-level Python jobs appear — no duplicates, no noise.

## Sources monitored

| Platform | Type | Focus |
|----------|------|-------|
| RemoteOK | API | Remote worldwide |
| Remotive | API | Remote software dev |
| Arbeitnow | API | Europe + remote |
| Himalayas | API | 100% remote |

## Run locally

**Requirements:** Python 3.10+
```bash
git clone https://github.com/aminooo101/Scrape
cd Scrape/job-scraper
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your credentials
python main.py
```

## Configuration

Copy `.env.example` to `.env` and fill in your values:
```
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=your_app_password   # Google App Password, not your real password
EMAIL_RECEIVER=your@gmail.com
KEYWORDS=python junior,entry level python,junior backend
```

## Project structure
```
job-scraper/
├── main.py        # scheduler + orchestrator
├── scraper.py     # fetches jobs from 4 APIs
├── storage.py     # deduplication via seen_jobs.json
├── notifier.py    # builds and sends email alerts
├── .env.example   # config template
└── requirements.txt
```

## How it works

1. `scraper.py` calls each job board API and normalises all results to the same format
2. `storage.py` compares against previously seen job IDs — only new ones pass through
3. `notifier.py` sends an email with title, company, and direct application link
4. `main.py` runs this on startup and then every day at 09:00

## Tech stack

requests · python-dotenv · schedule · smtplib · BeautifulSoup4
EOF

git add job-scraper/README.md
git commit -m "docs: add README for job scraper"
git push origin main
