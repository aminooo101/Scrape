import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_alert(jobs: list[dict]):
    if not jobs:
        return

    sender   = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')
    receiver = os.getenv('EMAIL_RECEIVER')

    lines = [f"Found {len(jobs)} new Python jobs:\n"]
    for job in jobs:
        lines.append(f"- {job['title']} at {job['company']}\n")
        url = job['url'] if job['url'] else "No link available"
        lines.append(f"  {url}\n")

    msg = MIMEMultipart()
    msg['From']    = sender
    msg['To']      = receiver
    msg['Subject'] = "New Python Jobs Found"
    msg.attach(MIMEText(''.join(lines)))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        print(f"Sent email alert for {len(jobs)} new jobs")