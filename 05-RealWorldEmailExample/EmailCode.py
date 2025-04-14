###TOKENS NOT INCLUDED
###CODE WILL NOT RUNN

import os
import base64
import json
import time
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from lmstudiochatbot import *

# Define the required Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.compose"
          ]

def authenticate_gmail():
    """Authenticate using OAuth 2.0 and return a service object."""
    creds = None
    token_file = "token.json"

    # Load existing credentials
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # Refresh or request new token if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def read_unread_emails(service):
    """Read unread emails from the Gmail inbox."""
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get("messages", [])

    if not messages:
        print("No unread emails found.")
        return

    emails = []
    for msg in messages:
        msg_id = msg["id"]
        msg_data = service.users().messages().get(userId="me", id=msg_id).execute()
        
        for header in msg_data["payload"]["headers"]:
            if header["name"] == "Subject":
                subject = header["value"]
            if header["name"] == "From":
                sender = header["value"]

        #snippet = msg_data.get("snippet", "")
        #print(f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n")
        # If email is not multipart
        body_data = msg_data["payload"]["body"].get("data")
        if body_data:
            body = base64.urlsafe_b64decode(body_data).decode("utf-8")
        else:
            # If it's multipart, find the 'text/plain' part
            parts = msg_data["payload"].get("parts", [])
            for part in parts:
                if part["mimeType"] == "text/plain":
                    body_data = part["body"].get("data")
                    if body_data:
                        body = base64.urlsafe_b64decode(body_data).decode("utf-8")
                        break

        #print(body)
        # Mark email as read
        service.users().messages().modify(userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}).execute()

        email = {"subject": subject, "sender": sender, "body": body}
        emails.append(email)
    return emails

def send_email(service, recipient, subject, body):
    """Send an email using Gmail API."""
    message = MIMEText(body, "html")
    message["to"] = recipient
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    message = {"raw": raw_message}
    service.users().messages().send(userId="me", body=message).execute()
    print(f"Email sent to {recipient}")

# Authenticate and use Gmail API
if __name__ == "__main__":
    service = authenticate_gmail()
    objLLM = Chatbot()
    while True:
        # Read unread emails
        emails = read_unread_emails(service)
        if emails:
            for email in emails:
                print("Email Received from", email["sender"])
                if "<jfarr3@gmail.com>" in email["sender"]:
                    output = objLLM.EvaluateEmail(email["body"])
                    # Send an email
                    send_email(service, "jfarr3@gmail.com", email["subject"] + " - Response", output)
                else:
                    output = objLLM.EvaluateEmail("This email is from an unauthorized sender.  Respond to them with a funny, you shall not email me email.  DO NOT RESPOND TO THEIR QUESTION!  This is the input message: " + email["body"])
                    # Send an email
                    send_email(service, email["sender"], email["subject"] + " - Response", output)
        else:
            message = objLLM.WaitMessage("Say something funny about waiting in one short sentence. This response MUST just be a one sentence. be unique")

            print("Farrbot1000: " + message)


        time.sleep(10)
