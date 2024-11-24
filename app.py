import base64
from flask import Flask, render_template, jsonify,request
from google_api import check_new_messages
from services import get_gmail_service,get_tasks_service
from summary import summarize
from googleapiclient.errors import HttpError

import os

app = Flask(__name__)

emails=[]
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/inbox')
def inbox():
    global emails
    emails = check_new_messages()
    print(emails)
    return jsonify(emails)

@app.route('/summary', methods=['GET'])
def load_summary():
    global emails
    email_summaries=summarize(emails)
    return jsonify(email_summaries)

@app.route('/logout', methods=['POST'])
def logout():
    token_path = 'token.json'
    if os.path.exists(token_path):
        os.remove(token_path)
        return jsonify({'message': 'Logged out successfully'}), 200
    else:
        return jsonify({'message': 'No token found to delete'}), 404

def create_message(to, subject, body):
    mime_message = f"From: me\nTo: {to}\nSubject: {subject}\n\n{body}"
    raw_message = base64.urlsafe_b64encode(mime_message.encode()).decode()
    
    return {'raw': raw_message}
    
@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    to_email = data['toEmail']
    subject = data['subject']
    body = data['body']
    
    try:
        service = get_gmail_service()
        message = create_message(to_email, subject, body)
        send_message = service.users().messages().send(userId='me', body=message).execute()
        
        return jsonify({'success': True, 'messageId': send_message['id']})
    
    except HttpError as error:
        return jsonify({'success': False, 'error': str(error)})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    service = get_tasks_service()
    try:
        result = service.tasks().list(tasklist='@default').execute()
        tasks = result.get('items', [])
        
        if not tasks:
            return jsonify({"message": "No tasks found."}), 200
        else:
            return jsonify(tasks), 200
    except HttpError as error:
        return jsonify({"error": f"An error occurred: {error}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
