import logging.config
import time

import pika

from config.logger_config import LOGGING_CONFIG
from config.settings import RabbitMQSettings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('app_consumer')


rabbit_config = RabbitMQSettings()
credentials = pika.PlainCredentials(rabbit_config.default_user, rabbit_config.default_pass.get_secret_value())
connection_host = pika.ConnectionParameters(host=rabbit_config.host, credentials=credentials)
connection = pika.BlockingConnection(connection_host)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
logger.info(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    logger.info(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    logger.info(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
