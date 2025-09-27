from fastapi import FastAPI
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
import os

app = FastAPI()

IMAP_HOST = "imap.ionos.com"
SMTP_HOST = "smtp.ionos.com"
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


@app.get("/")
def home():
    return {"status": "Email MCP Server running"}


@app.get("/emails")
def fetch_emails(limit: int = 5):
    conn = imaplib.IMAP4_SSL(IMAP_HOST)
    conn.login(EMAIL, PASSWORD)
    conn.select("INBOX")

    # Fetch the latest emails
    status, data = conn.search(None, "ALL")
    mail_ids = data[0].split()[-limit:]
    emails = []
    for mid in reversed(mail_ids):
        status, msg_data = conn.fetch(mid, "(RFC822)")
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)

        snippet = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        snippet = payload[:200].decode(errors="ignore")
                    break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                snippet = payload[:200].decode(errors="ignore")

        emails.append({
            "from": msg["From"],
            "to": msg["To"],
            "subject": msg["Subject"],
            "snippet": snippet
        })

    conn.close()
    conn.logout()
    return {"emails": emails}


@app.post("/drafts")
def create_draft(to: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["From"] = EMAIL
    msg["To"] = to
    msg["Subject"] = subject

    # Save to Drafts using IMAP APPEND
    imap = imaplib.IMAP4_SSL(IMAP_HOST)
    imap.login(EMAIL, PASSWORD)
    imap.append("Drafts", "\\Draft", None, msg.as_bytes())
    imap.logout()

    
    
@app.post("/send")
def send_email(to: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["From"] = EMAIL
    msg["To"] = to
    msg["Subject"] = subject

    smtp = smtplib.SMTP(SMTP_HOST, 587)
    smtp.starttls()
    smtp.login(EMAIL, PASSWORD)
    smtp.sendmail(EMAIL, [to], msg.as_string())
    smtp.quit()

    return {"status": "email_sent"}
 
