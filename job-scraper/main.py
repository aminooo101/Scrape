import schedule,time,os
from dotenv import load_dotenv
from scraper import get_jobs
from storage import filter_new_jobs
from notifier import send_alert

load_dotenv()
def run():
    keywords = os.getenv('KEYWORD', 'python').split(',')
    # Trim whitespace just in case there are spaces after commas in .env
    keywords = [k.strip() for k in keywords] 
    
    print(f"Searching for keywords: {keywords}")
    
    jobs = get_jobs(keywords)
    print(f"Total jobs matching keywords from API: {len(jobs)}") # DEBUG LINE
    
    new_jobs = filter_new_jobs(jobs)
    print(f"Found {len(new_jobs)} new jobs")
    
    if new_jobs:
        send_alert(new_jobs)

run()
schedule.every(1).hours.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)


