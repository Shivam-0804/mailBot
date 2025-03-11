# MailBot

**MailBot** is an intelligent mail management system designed to improve productivity by automating email organization, task scheduling, and spam filtering. By leveraging Natural Language Processing (NLP) and Google APIs, MailBot efficiently extracts tasks from emails, creates calendar events, and filters spam to streamline professional email management.

## About the Project
The project comprises various interconnected modules designed to automate key email management tasks:

- **Email Parsing:** Extracts relevant information like tasks, deadlines, and sender details from incoming emails.
- **Date and Time Recognition:** Identifies dates from email text using NLP techniques to create scheduled tasks.
- **Task Scheduling:** Automatically schedules identified tasks in Google Calendar.
- **Spam Filtering:** Utilizes machine learning algorithms to filter spam efficiently.
- **User Interface:** Provides an intuitive UI to manage emails, view tasks, and track calendar events.

## Features
- Automated Email Parsing
- Intelligent Date and Time Recognition
- Google Calendar Integration for Task Scheduling
- Spam Filtering with Machine Learning
- Simple and User-Friendly Interface
- Enhanced Productivity for Professionals

## Technologies Used
- **Python:** For NLP tasks, including text processing, date extraction, and spam filtering.
- **NLP Libraries:** SpaCy, scikit-learn
- **Google APIs:** Google Mail API, Google Calendar API
- **Frontend Development:** HTML, CSS, Pug
- **Database:** MongoDB
- **Backend Development:** Node.js (for API integration and data handling)

## Getting Started
To run MailBot locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd MailBot
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use 'env\Scripts\activate'
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys:**
   - Set up your Google Mail API and Google Calendar API keys.
   - Add these keys in your environment variables or a `.env` file.

5. **Import Database Schema:**
   - Create a MongoDB database and import the schema provided in the project files.

6. **Run the Project:**
   ```bash
   python main.py
   ```

7. **Access the Application:**
   Open your web browser and go to `http://localhost:5000` (or the specified port).

## Contributors
- Shivam-0804
- abhis1n
- ocidemus

## License
This project is licensed under the MIT License.

## Acknowledgments
Special thanks to **Dr. Sakshi Gupta** for her guidance throughout the project. Appreciation to the team for their dedication and effort in developing MailBot.

