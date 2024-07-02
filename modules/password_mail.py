from PySide6.QtWidgets import QLabel, QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
import os
import base64
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import mysql.connector

# Path to the client secret JSON file
CLIENT_SECRET_FILE = 'credential.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_connection():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='nmap'
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Failed to create Gmail service: {e}")
        return None

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message Id: {message['id']}")
        return message
    except Exception as error:
        print(f"An error occurred: {error}")
        return None

class EmailVerificationDialog(QDialog):
    def __init__(self, parent=None):
        super(EmailVerificationDialog, self).__init__(parent)
        self.setWindowTitle("Email Verification")
        self.setGeometry(100, 100, 300, 150)
        self.setStyleSheet("background-color: grey;")
        
        layout = QVBoxLayout()

        self.title = QLabel("Email Verification", self)
        self.title.setStyleSheet("""
                        QLabel {
                                color: black;
                                font-size: 24px;
                                font-style: italic;
                                font-weight: bold;
                        }
                        """)        
        layout.addWidget(self.title)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Type your email")
        layout.addWidget(self.email_input)

        button_layout = QHBoxLayout()
        self.send_button = QPushButton("Send Code", self)
        self.send_button.setStyleSheet("background-color: #000; color:rgba(255, 255, 255, 210); border-radius:5px;")
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setStyleSheet("background-color: #000; color:rgba(255, 255, 255, 210); border-radius:5px;")
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.cancel_button.clicked.connect(self.reject)
        self.send_button.clicked.connect(self.send_mail)

    def send_mail(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, "Input Error", "Please enter an email address.")
            return

        mydb = create_connection()
        if not mydb:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return

        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT Username, Password FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            cursor.close()
            mydb.close()

            if result:
                username, user_password = result
                service = get_gmail_service()
                if not service:
                    QMessageBox.critical(self, "Gmail Error", "Failed to connect to Gmail service.")
                    return

                sender_email = "NetMoon_Version_1@gmail.com"
                subject = "Login information"
                body = f"Hello {username},\n\nYour password is: {user_password}."
                message = create_message(sender_email, email, subject, body)
                send_message(service, 'me', message)
                QMessageBox.information(self, "Email Sent", f"Login Information sent succesfuly to : {email}!")
                self.accept()
            else:
                QMessageBox.warning(self, "Database Error", f"No account found for {email}. Please verify your account email.")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {err}")
