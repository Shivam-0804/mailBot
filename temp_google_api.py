import base64
from services import get_gmail_service
from googleapiclient.errors import HttpError
from google_tasks import create_task,convert_date_to_iso
from services import get_tasks_service
from schedular import extract_event_info

from spam_filter import model, vectorizer

def extract_message_body(payload):
    parts = payload.get("parts", [])
    if parts:
        for part in parts:
            if part["mimeType"] == "text/plain":
                data = part["body"]["data"]
                return base64.urlsafe_b64decode(data).decode()
            elif part["mimeType"] == "text/html":
                data = part["body"]["data"]
                return base64.urlsafe_b64decode(data).decode()
    elif "body" in payload and "data" in payload["body"]:
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode()
    return "No message body found."

def check_new_messages(max_results=20):
    service = get_gmail_service()
    task_service= get_tasks_service()
    try:
        results = service.users().messages().list(
            userId="me", labelIds=["INBOX"], maxResults=max_results
        ).execute()

        if 'messages' not in results:
            print("No messages found.")
            return []

        messages = results['messages']
        emails = []

        if messages:
            batch = service.new_batch_http_request()

            def handle_message_response(request_id, response, exception):
                if exception:
                    print(f"Error fetching message {request_id}: {exception}")
                else:
                    message = response.get("payload", {})
                    headers = message.get("headers", [])
                    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
                    from_address = next((header['value'] for header in headers if header['name'] == 'From'), "Unknown Sender")
                    message_body = extract_message_body(message)

                    input_data_features = vectorizer.transform([message_body])
                    prediction = model.predict(input_data_features)[0]
                    if prediction == 1:
                        label_ids = message.get("labelIds", [])
                        if "UNREAD" in label_ids:
                            event_info = extract_event_info(message_body)

                            if event_info['tasks'] and event_info['date_time']:
                                due_date = event_info['date_time'].isoformat() + 'Z'
                                tasks = event_info['tasks'][0]
                                create_task(task_service, tasks, due_date)

                        emails.append({
                            "sender": from_address,
                            "subject": subject,
                            "body": message_body
                        })

            for i, message_info in enumerate(messages):
                message_id = message_info['id']
                batch.add(service.users().messages().get(userId="me", id=message_id, format="full"), 
                          callback=lambda request_id, response, exception: handle_message_response(request_id, response, exception))

            batch.execute()

        return emails

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []
