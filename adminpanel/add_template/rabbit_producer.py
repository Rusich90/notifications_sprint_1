import sys

import pika

from config.settings import RabbitMQSettings


rabbit_config = RabbitMQSettings()
credentials = pika.PlainCredentials(rabbit_config.default_user, rabbit_config.default_pass.get_secret_value())
connection_host = pika.ConnectionParameters(host=rabbit_config.host, credentials=credentials)
connection = pika.BlockingConnection(connection_host)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
connection.close()
