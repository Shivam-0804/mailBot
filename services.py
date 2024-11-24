import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/tasks"
]

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def get_tasks_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("tasks", "v1", credentials=creds)

def create_task(service, title, due_date):
    task = {
        'title': title,
        'due': due_date
    }
    try:
        result = service.tasks().insert(tasklist='@default', body=task).execute()
        print(f"Task created: {result['title']} due on {result['due']}")
    except HttpError as error:
        print(f"An error occurred while creating the task: {error}")

def convert_date_to_iso(date_str):
    try:
        task_due_date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return task_due_date.isoformat() + 'Z'
    except ValueError:
        print("Invalid date format. Please use 'YYYY-MM-DD HH:MM:SS'")
        return None

def main():
    gmail_service = get_gmail_service()
    tasks_service = get_tasks_service()
    title = input("Enter the task title (subject): ")
    due_date_str = input("Enter the due date (YYYY-MM-DD HH:MM:SS): ")
    due_date = convert_date_to_iso(due_date_str)
    if due_date:
        create_task(tasks_service, title, due_date)
    else:
        print("Invalid date format. Task not created.")

if __name__ == "__main__":
    main()
