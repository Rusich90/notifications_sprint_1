from django.db import models
from db.database import PostgresDataBase
from rb.rabbit_producer import RBPublisher
from base64 import b64encode
from config.logger_config import LOGGING_CONFIG
import json
import logging

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('app')
MAX_CHUNK_SIZE = 2


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

    def Send(self, *args, **kwargs):
        def create_message_file(file_html):
            base64_bytes = b64encode(file_html)
            base64_string = base64_bytes.decode('utf-8')
            return base64_string

        conn = RBPublisher('_emails.send-all')
        conn.channel.queue_declare(queue='_emails.send-all', durable=True)
        message_file = create_message_file((self.mail_template).read())
        base = PostgresDataBase()
        users = base.get_all_users()
        end_item = 0
        while end_item < len(users):
            print(end_item)
            first_item = end_item
            end_item += (end_item + MAX_CHUNK_SIZE) % len(users)
            print(end_item)
            if end_item < 1:
                break
            chunk = users[first_item:end_item]
            logger.info('Sent users %s - %s', first_item, end_item)
            conn.public(json.dumps(
                {'user_list': chunk, 'subject': self.subject, 'file': message_file}))
        conn.close_connection()


class SMS(models.Model):
    Name = models.CharField(
        max_length=255,
    )
    user_filter = models.CharField(
        max_length=255,
    )
    text = models.CharField(
        max_length=140, default=''
    )

    list_schedule = models.TextChoices('', 'Once Daily Weekly Monthly')
    sms_schedule = models.CharField(choices=list_schedule.choices, max_length=255)

    def save(self, *args, **kwargs):
        pass


class Push(models.Model):
    Name = models.CharField(
        max_length=255,
    )
    user_filter = models.CharField(
        max_length=255,
    )
    text = models.CharField(
        max_length=140, default=''
    )

    list_schedule = models.TextChoices('', 'Once Daily Weekly Monthly')
    push_schedule = models.CharField(choices=list_schedule.choices, max_length=255)

    def save(self, *args, **kwargs):
        pass
