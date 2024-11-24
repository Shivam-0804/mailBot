from googleapiclient.errors import HttpError
import datetime
from services import get_tasks_service
from dateutil import parser


def create_task(service, title, due_date):
    try:
        task = {
            'title': title,
            'due': due_date
        }
        result = service.tasks().insert(tasklist='@default', body=task).execute()
        print(f"Task created: {result['title']} due on {result['due']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def convert_date_to_iso(date_str):
    try:
        task_due_date = parser.parse(date_str)
        return task_due_date.isoformat()
    except (ValueError, TypeError):
        print("Invalid date format.")
        return None

def display_tasks(service):
    try:
        result = service.tasks().list(tasklist='@default').execute()
        tasks = result.get('items', [])
        
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                title = task['title']
                due = task.get('due', 'No due date')
                print(f"Task: {title}, Due: {due}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    service = get_tasks_service()
    
    if not service:
        print("Failed to authenticate with Google API.")
        return

    action = input("Would you like to create a task or view all tasks? (create/view): ").strip().lower()
    
    if action == 'create':
        title = input("Enter the task title (subject): ")
        due_date_str = input("Enter the due date (YYYY-MM-DD HH:MM:SS): ")
        due_date = convert_date_to_iso(due_date_str)
        
        if due_date:
            create_task(service, title, due_date)
        else:
            print("Invalid date. Task not created.")
    elif action == 'view':
        display_tasks(service)
    else:
        print("Invalid option. Please choose 'create' or 'view'.")

if __name__ == '__main__':
    main()
