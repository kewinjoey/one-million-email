# One-million-email

## About the project:

The program will send emails to a list of recipients extracted from a CSV file using Gmail API and OAuth 2.0 authentication.
Since Gmail API restricts the number of recipients per email, it is roughly 500 external(other email services) recipients and 
2000 Gmail recipients can be included in single email. I have assumed the recipients are external and, the program will limit 
to 500 recipients in Bcc per email and it will iterate to 1 Mio recipients or the maximum number of recipients.The recipients 
are in 'Bcc' field instead of 'TO' field, to avoid disclosure of Email ID's.


## Prerequisites:

Python 3\
httplib2\
oauth2client\
base64\
mimetypes\
pandas\
time


## Note:

The snippet, which sends the email is commented out in the program and replaced by sleep function to wait for half a second.
During first run of the program, a new window will open up for Gmail authorization, Authorization is done only once.





