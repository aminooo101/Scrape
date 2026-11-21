# Job Scraper — Python Automated Job Alerts

Scrapes 4 remote job boards daily, filters by keywords and seniority, deduplicates results, and sends email alerts only when new junior-level Python jobs appear.

## Sources monitored

| Platform   | Type | Focus              |
|------------|------|--------------------|
| RemoteOK   | API  | Remote worldwide   |
| Remotive   | API  | Remote software    |
| Arbeitnow  | API  | Europe + remote    |
| Himalayas  | API  | 100% remote        |

## Installation & Run

```bash
git clone https://github.com/aminooo101/Scrape
cd Scrape/job-scraper
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Gmail app password and keywords
python main.py
```

The script runs once on startup and then every day at 09:00.

## Configuration (.env)

```
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your@gmail.com
KEYWORDS=python junior,entry level python,junior backend
```

## Project structure

```
job-scraper/
├── main.py        # scheduler + orchestrator
├── scraper.py     # fetches and normalises jobs from 4 APIs
├── storage.py     # deduplication via seen_jobs.json
├── notifier.py    # builds and sends email alerts
├── .env.example   # config template
└── requirements.txt
```

## How it works

1. `scraper.py` calls each job board API and normalises results
2. `storage.py` compares against previously seen job IDs
3. `notifier.py` sends an email only for new matching jobs
4. `main.py` schedules the process daily

## Tech stack

requests · python-dotenv · schedule · smtplib

## Author

Amin Hadian · [github.com/aminooo101](https://github.com/aminooo101)
