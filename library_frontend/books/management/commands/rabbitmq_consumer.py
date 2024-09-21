# your_app/rabbitmq_consumer.py
import pika
import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import Book  

class Command(BaseCommand):
    help = 'Consume messages from RabbitMQ'

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        channel.queue_declare(queue='book_updates', durable=True)

        def callback(ch, method, properties, body):
            book_data = json.loads(body)
            self.create_book(book_data)
            ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

        channel.basic_consume(queue='book_updates', on_message_callback=callback)

        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def create_book(self, book_data):
        book, created = Book.objects.get_or_create(
            title=book_data['title'],
            author=book_data['author'],
            publisher=book_data['publisher'],
            category=book_data['category'],
            defaults={'status': 'available'}
        )
        if created:
            print(f"New book added: {book.title} by {book.author}")
        else:
            print(f"Book already exists: {book.title}")
