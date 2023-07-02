import pika
import db.connect
from db.models import Contact
import json


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='SMS_queue', durable=True)


def send_sms(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f'Sending SMS to {contact.phone}...')
    # Тут можна реалізувати функціонал надсилання sms
    contact.is_sent = True
    contact.save()
    print(f'SMS sent to {contact.phone}')


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    send_sms(contact_id)


channel.basic_consume(queue='SMS_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
