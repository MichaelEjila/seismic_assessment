# your_app/rabbitmq.py
import pika
import json

def send_book_added_message(book_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='book_updates', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='book_updates',
        body=json.dumps(book_data)  # Convert book data to JSON string
    )

    connection.close()
