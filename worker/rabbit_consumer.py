import logging.config
import pika
import json

from config.logger_config import LOGGING_CONFIG
from config.settings import RabbitMQSettings
from emails import Emails
from base64 import b64decode

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('app_consumer')

rabbit_config = RabbitMQSettings()
credentials = pika.PlainCredentials(rabbit_config.default_user, rabbit_config.default_pass.get_secret_value())
QUEUE = '_emails.send-all'


class RBConsumer():
    CONNECTION_HOST = pika.ConnectionParameters(host=rabbit_config.host, socket_timeout=15, credentials=credentials)

    def __init__(self, routing_key):
        self.connection = pika.BlockingConnection(self.CONNECTION_HOST)
        self.channel = self.connection.channel()
        logger.info('Connecting to %s', self.CONNECTION_HOST)
        self.routing_key = routing_key

    def receive(self):
        def callback(ch, method, properties, body):
            data = json.loads(body.decode())
            logger.info(" [x] Decoded %r" % data['first_name'])
            self.send_mail(data)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='_emails.send-all', on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()
        self.connection = None
        logger.info('Stopped')
    def send_mail(self, data):
        filestring = data['file']
        file_bytes = filestring.encode('utf-8')
        file = b64decode(file_bytes)
        with open("mail.html", "wb") as binary_file:
            binary_file.write(file)
        email = Emails()
        email.send_email(data)
