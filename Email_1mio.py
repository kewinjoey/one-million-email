import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email import encoders
from oauth2client import file
import mimetypes
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery  
import pandas as pd
import time


#Getting the CLIENT_ID and the scope and the credentials
def get_credentials():
    home_dir = os.path.expanduser('~') 
    credential_dir = os.path.join(home_dir, '.credentials') 
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir) 
    credential_path = os.path.join(credential_dir, 'cred send mail.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        client_secure = 'client_secret.json'
        App_name = 'One million Email'
        scopes = 'https://www.googleapis.com/auth/gmail.send'
        flow = client.flow_from_clientsecrets(client_secure, scopes)
        flow.user_agent = App_name
        credentials = tools.run_flow(flow, store)

    return credentials


#establishing a connection to gmail, usually the current email logged in is authorised once by the program
def create_connection(sender,to,subject,message_text_plain,message_text_html):
    credentials = get_credentials()
    http = httplib2.Http()
    http = credentials.authorize(http)        
    service = discovery.build('gmail', 'v1', http=http)
    message_to_send = create_message(sender, to, subject, message_text_html, message_text_plain)
    send_Message(service, "me", message_to_send, message_text_plain)

#Creating a message and encoding to base 64
def create_message (sender,to,subject,message_text_html,message_text_plain):
    message = MIMEMultipart('alternative') 
    message['Subject'] = subject
    message['From'] = sender
    message['Bcc'] = to #the group of email ID's are placed in Bcc to avoid privacy issues
    message.attach(MIMEText(message_text_plain, 'plain'))
    message.attach(MIMEText(message_text_html, 'html'))
    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    raw_message = raw_message.decode()
    body  = {'raw': raw_message}
    return body


#Sending the message,but in this scenario it is commented out to execute half a second
def send_Message(service,user_id,body,message_text_plain):
    try:
        #message_sent = (service.users().messages().send(userId=user_id, body=body).execute())
        #message_id = message_sent['id']
        time.sleep(0.5)
        #print (f'Message sent \n\n Message Id: {message_id}\n\n Message:\n\n {message_text_plain}')
    except errors.HttpError as error:
        print (f'An error occurred: {error}')

#Main function containing the essential parameters and sending the mail to individial group of 500 emails ID's(the email ID's are inserted in the BCC field
#to enhance privacy)
#since Goodle Gmail API supports only 500 external email recipients
def main():
    count=0
    total_to=''
    sender = "kewinjoey@gmail.com"
    subject = "Testing"
    message_text_html  = r'Hi<br/><b>Sample Email</b>'
    message_text_plain = "Hi\nPlain Email"
    emails = pd.read_csv("emails.csv",delimiter = ',')
    to=' '
    for id in emails:
        to = str(id)+','+to

    to=str(to)
    to=to[:-2]
    individual_id=to.split(',')
    length=len(individual_id)
    for id500 in individual_id:
        if count<500 and length>1:
            total_to =id500+','+total_to
            count+=1
            length-=1

        else :
            total_to =id500+','+total_to
            create_connection(sender,total_to,subject,message_text_plain,message_text_html)
            count=0

if __name__ == '__main__':
        main()
