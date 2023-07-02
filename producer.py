import pika
from faker import Faker
import db.connect
from random import choice
from db.models import Contact

import json


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='SMS_queue', durable=True)


def generate_contacts(num_contacts):
    fake = Faker('en-US')
    contacts = []
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        email_push = choice([False, True])
        contact = Contact(full_name=full_name, email=email,
                          phone=phone, email_push=email_push)
        contact.save()
        contacts.append(contact)
    return contacts


contacts = generate_contacts(15)


for contact in contacts:
    message = {
        'contact_id': str(contact.id)
    }
    channel.basic_publish(
        exchange='',
        routing_key='email_queue' if contact.email_push else 'SMS_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        )
    )


connection.close()
