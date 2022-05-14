import logging.config

import backoff
import pika
from pika.exceptions import AMQPConnectionError

from callbacks import welcome_email, all_email
from config.logger_config import LOGGING_CONFIG
from config.settings import RabbitMQSettings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('app_consumer')


class Consumer:
    def __init__(self, connection_host):
        self.connection_host = connection_host
        self.connection = None

    def start_receive(self):
        channel = self._connection()
        channel.basic_qos(prefetch_count=1)

        channel.queue_declare(queue='_emails.send-all', durable=True)
        channel.basic_consume(queue='_emails.send-all', on_message_callback=all_email)

        channel.queue_declare(queue='welcome_email', durable=True)
        channel.basic_consume(queue='welcome_email', on_message_callback=welcome_email)

        logger.info('Consumer waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    @backoff.on_exception(backoff.expo, AMQPConnectionError)
    def _connection(self):
        self.connection = pika.BlockingConnection(connection_host)
        return self.connection.channel()

    def close_connection(self):
        self.connection.close()
        self.connection = None
        logger.info('Stopped')


if __name__ == '__main__':
    config = RabbitMQSettings()
    credentials = pika.PlainCredentials(config.default_user, config.default_pass.get_secret_value())
    connection_host = pika.ConnectionParameters(host=config.host, credentials=credentials)
    consumer = Consumer(connection_host)
    try:
        consumer.start_receive()
    except KeyboardInterrupt:
        consumer.close_connection()
