import json
import pika

from cafe_service import crud
from cafe_service.models import Coffee
from cafe_service.schemas import CoffeeResponse

RABBITMQ_HOST = "51.250.26.59"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest123"
QUEUE_NAME = "coffee_shop_actions"


def callback(channel, method, properties, body):
    print("Получение данных!")
    message = json.loads(body)
    action = message.get('action')
    coffee_data = message.get('coffee')
    coffee_response = CoffeeResponse(**coffee_data)
    coffee = Coffee(
        id=coffee_response.id,
        name=coffee_response.name,
        description=coffee_response.description,
        price=coffee_response.price,
        is_available=coffee_response.is_available
    )
    print(coffee.id)
    if action == "add":
        crud.add_coffee_to_all_shops(coffee)
    elif action == "delete":
        crud.delete_coffee(coffee)
        coffee_shops = crud.get_all_coffee_shops()
        for shop in coffee_shops:
            crud.remove_coffee_from_coffee_shop(shop.id, coffee.id)
    elif action == "toggle_availability":
        crud.coffee_availability(coffee)


def listen_queue():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(QUEUE_NAME)
    channel.basic_consume(
        queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True
    )
    print('Ожидание сообщений. Для выхода нажмите CTRL+C')
    channel.start_consuming()
