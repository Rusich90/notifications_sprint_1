from django.db import models
from db.database import PostgresDataBase
from rb.rabbit_producer import RBPublisher
from base64 import b64encode
from config.logger_config import LOGGING_CONFIG
import json
import logging

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('app')


class Mailing(models.Model):
    mailing = models.CharField(
        max_length=255,
    )
    user_filter = models.CharField(
        max_length=255,
    )
    subject = models.CharField(
        max_length=255, default=''
    )

    mail_template = models.FileField()
    list_schedule = models.TextChoices('', 'Once Daily Weekly Monthly')
    mail_schedule = models.CharField(choices=list_schedule.choices, max_length=255)

    def save(self, *args, **kwargs):
        def create_message_file(file_html):
            base64_bytes = b64encode(file_html)
            base64_string = base64_bytes.decode('utf-8')
            return base64_string

        conn = RBPublisher('_emails.send-all')
        conn.channel.queue_declare(queue='_emails.send-all', durable=True)
        message_file = create_message_file((self.mail_template).read())
        base = PostgresDataBase()
        users = base.get_all_users()

        for user in users:
            logger.info('Sent to %s', user['last_name'])
            print(user)
            conn.public(json.dumps(
                {'first_name': user['first_name'], 'last_name': user['last_name'], 'email': user['email'],
                 'subject': self.subject, 'file': message_file}))
        conn.close_connection()
        super().save(*args, **kwargs)
