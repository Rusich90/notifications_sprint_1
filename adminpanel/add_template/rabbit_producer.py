import logging.config
import sys

import pika

from config.logger_config import LOGGING_CONFIG
from config.settings import RabbitMQSettings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('app_producer')


rabbit_config = RabbitMQSettings()
credentials = pika.PlainCredentials(rabbit_config.default_user, rabbit_config.default_pass.get_secret_value())
connection_host = pika.ConnectionParameters(host=rabbit_config.host, credentials=credentials)
connection = pika.BlockingConnection(connection_host)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
logger.info(" [x] Sent %r" % message)
connection.close()