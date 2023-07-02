import pika
import db.connect
from db.models import Contact
import json


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='email_queue', durable=True)



def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f'Sending email to {contact.email}...')
    # Тут можна реалізувати функціонал надсилання email
    contact.is_sent = True
    contact.save()
    print(f'Email sent to {contact.email}')


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    send_email(contact_id)


channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
