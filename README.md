# Scrape

Python automation projects.

## Job Scraper

Automated job alerts that scrape four remote job boards, filter for junior-level Python roles, deduplicate results, and send daily email notifications.

See the full documentation and run instructions in the [`job-scraper`](job-scraper/) folder.

### Quick start

```bash
cd job-scraper
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your email credentials
python main.py
```

## Author

Amin Hadian · [github.com/aminooo101](https://github.com/aminooo101)
