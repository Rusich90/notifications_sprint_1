import logging.config
import pika

from config.settings import RabbitMQSettings
from config.logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('rb_producer')

rabbit_config = RabbitMQSettings()
credentials = pika.PlainCredentials(rabbit_config.default_user, rabbit_config.default_pass.get_secret_value())

class RBPublisher():
    CONNECTION_HOST = pika.ConnectionParameters(host=rabbit_config.host, credentials=credentials)

    def __init__(self, routing_key):
        self.connection = pika.BlockingConnection(self.CONNECTION_HOST)
        self.channel = self.connection.channel()
        logger.info('Connecting to %s', self.CONNECTION_HOST)
        self.routing_key = routing_key

    def public (self, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        logger.info("Sent message")

    def close_connection (self):
        self.connection.close()
        self.connection = None
        logger.info('Stopped')
