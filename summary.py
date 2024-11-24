import time
from googleapiclient.errors import HttpError

from summarizer import summarize_extractive

from services import get_gmail_service

email_summaries = []

def summarize(emails):
    for email in emails:
        summary = summarize_extractive(email['body'])
        email_summary = {
            "from": email['sender'],
            "subject": email["subject"],
            "summary": summary,
        }
        email_summaries.append(email_summary)
    return email_summaries

def send_email_summary(service):
    if not email_summaries:
        print("No summaries available to send.")
        return

    summary_text = "\n\n".join([f"From: {email['from']}\nSubject: {email['subject']}\nSummary: {email['summary']}" for email in email_summaries])

    to_email = "your-email@example.com"
    subject = "Summary of the Last 20 Emails"

    email_data = {
        'to': to_email,
        'subject': subject,
        'body': summary_text
    }

    send_email(service, email_data)

def send_email(service, email_data):
    try:
        message = create_message(email_data['to'], email_data['subject'], email_data['body'])
        send_message(service, "me", message)
        print(f"Summary email sent to {email_data['to']}.")
    except Exception as error:
        print(f"An error occurred while sending the email: {error}")

def create_message(to, subject, body):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import base64

    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    msg = MIMEText(body)
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {'raw': raw_message}

def send_message(service, sender, message):
    try:
        message = service.users().messages().send(userId=sender, body=message).execute()
        print(f"Message sent: {message['id']}")
        return message
    except HttpError as error:
        print(f"An error occurred while sending message: {error}")

def main():
    service = get_gmail_service()

    while True:
        summarize(service)
        send_email_summary(service)
        print("Waiting for the next check...")
        time.sleep(60)

if __name__ == "__main__":
    main()

