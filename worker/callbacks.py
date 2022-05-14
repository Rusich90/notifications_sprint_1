import json
import logging.config

from config.logger_config import LOGGING_CONFIG
from emails.emails import Emails
from short_url import ShortUrl
from base64 import b64decode
from db.database import PostgresDataBase

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('app_consumer')


def welcome_email(ch, method, properties, body):
    logger.info("Received message from welcome_email queue")
    user = json.loads(body.decode())
    logger.info(user)

    short_url = ShortUrl()
    link = short_url.get_short_url(user['id'])
    data = {
        'subject': 'Привет!',
        'recipients': [user['email']],
        'html_template': 'welcome_mail.html',
        'full_name': f'{user["first_name"]} {user["last_name"]}',
        'link': link,
        'image': 'https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7-96e1c2d387fa.png'
    }
    emails = Emails()
    emails.send_email(data)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info("Done")


def all_email(ch, method, properties, body):
    logger.info("Received message from all_email queue")
    data = json.loads(body.decode())
    logger.info(data['user_list'])
    filestring = data['file']
    file_bytes = filestring.encode('utf-8')
    file = b64decode(file_bytes)
    with open("emails/templates/mail.html", "wb") as binary_file:
        binary_file.write(file)
    base = PostgresDataBase()
    emails = Emails()
    for user_id in data['user_list']:
        user = base.get_user(user_id['id'])
        data_to_mail = {'subject' : data['subject'], 'recipients' : user['email'], 'first_name' : user['first_name'], 'last_name' : user['last_name']}
        emails.send_email(data_to_mail)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info("Done")
