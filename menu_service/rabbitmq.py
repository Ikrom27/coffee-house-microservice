import json

import pika

RABBITMQ_HOST = "51.250.26.59"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest123"
QUEUE_NAME = "coffee_shop_actions"


def publish(message: dict):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(QUEUE_NAME)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(message)
    )
    print("Сообщение отпралено")
    channel.close()


def send_coffee_action(coffee: dict, action: str):
    publish({
        "coffee": coffee,
        "action": action
    })

