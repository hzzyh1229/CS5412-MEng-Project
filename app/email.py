import smtplib
import logging

import azure.functions as func
from azure.cosmos import CosmosClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Positions'
container = database.get_container_client(CONTAINER_NAME)
CONTAINER_NAME2 = 'Applications'
application_container = database.get_container_client(CONTAINER_NAME2)

sender_address = 'cs5154jobboard@outlook.com'
sender_pass = 'test5154'
receiver_address = ['sh2429@cornell.edu', 'hzzyh1229@outlook.com']
#Setup the MIME

    
def main(documents: func.DocumentList) -> str:
    logging.info("is running")
    if documents:
        company = documents[0]['company']
        # logging.info('Company name: %s', company)
        logging.info("-------------------------------------")
        print(company)
        email_info = list(application_container.query_items(
                        query='SELECT DISTINCT c.email FROM c WHERE c.company = @company', 
                        parameters=[dict(name = "@company", value = company)], 
                        enable_cross_partition_query=True))
        # print("!!!!!!!!!!!!!!!!!!!")
        print(email_info)

        mail_content = """ \
        Hi,
        
        There is a new job posting for company: {}.""".format(company)
        message = MIMEMultipart()
        message['From'] = sender_address
        # message['To'] = receiver_address
        message['Subject'] = 'Updates to jobs you might be interested in'   #The subject line
        # #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp-mail.outlook.com', port=587) #use gmail with port
        session.ehlo()
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
