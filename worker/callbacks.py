import json
import logging.config

from config.logger_config import LOGGING_CONFIG
from emails.emails import Emails
from short_url import ShortUrl

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
    logger.info(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info("Done")
