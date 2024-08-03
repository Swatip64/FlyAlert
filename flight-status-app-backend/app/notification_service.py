# app/notification_service.py

from .rabbitmq_service import channel, notification_queue

# Producer service to publish notifications
def publish_notification(message, notification_type):
    # Define the message payload
    notification_data = {
        'type': notification_type,
        'message': message
    }

    # Publish the message to the RabbitMQ queue
    channel.basic_publish(
        exchange='',
        routing_key=notification_queue,
        body=str(notification_data)
    )

    print(f"Published {notification_type} notification: {message}")

# Consumer service to process notifications
def consume_notifications():
    def callback(ch, method, properties, body):
        notification_data = eval(body.decode('utf-8'))
        notification_type = notification_data['type']
        message = notification_data['message']

        if notification_type == 'SMS':
            send_sms(message)
        elif notification_type == 'email':
            send_email(message)

    # Consume messages from the notification queue
    channel.basic_consume(
        queue=notification_queue,
        on_message_callback=callback,
        auto_ack=True
    )

    print('Waiting for notifications...')
    channel.start_consuming()

def send_sms(message):
    # Implement logic to send SMS notifications
    print(f"Sending SMS: {message}")

def send_email(message):
    # Implement logic to send email notifications
    print(f"Sending email: {message}")
