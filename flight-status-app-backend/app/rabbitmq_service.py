import pika
import json
from app import socketio

RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'notifications'

def consume_notifications():
    """
    Consume messages from the RabbitMQ queue and handle notifications.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        socketio.emit('notification', data, broadcast=True)

    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
