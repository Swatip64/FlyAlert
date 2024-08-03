import firebase_admin
from firebase_admin import messaging
import pika

def send_firebase_notification(title, body, token):
    """Send a push notification using Firebase Cloud Messaging."""
    # Ensure Firebase is initialized
    if not firebase_admin._apps:
        cred = firebase_admin.credentials.Certificate("path/to/your/firebase/credentials.json")
        firebase_admin.initialize_app(cred)

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    # Send the message
    response = messaging.send(message)
    print('Successfully sent message:', response)

def send_notification(message):
    """Send a notification using RabbitMQ."""
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='notifications')

    # Publish the message to the queue
    channel.basic_publish(exchange='', routing_key='notifications', body=message)
    print(" [x] Sent %r" % message)

    # Close the connection
    connection.close()

def consume_notifications():
    """Consume notifications from RabbitMQ and process them."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='notifications')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        # Here, you can process the message (e.g., send a push notification)

    channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
