import json

import aio_pika

from config.settings import RabbitMQSettings

config = RabbitMQSettings()


async def producer(user) -> None:
    connection = await aio_pika.connect_robust(
        host=config.host,
        login=config.default_user,
        password=config.default_pass.get_secret_value()
    )

    async with connection:

        channel = await connection.channel()
        queue = await channel.declare_queue("welcome_email", durable=True)

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(user).encode()),
            routing_key=queue.name,
        )
