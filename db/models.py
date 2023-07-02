from mongoengine import Document
from mongoengine.fields import BooleanField, StringField


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    email_push = BooleanField()  # True - send emails, False - send SMS
    is_sent = BooleanField(default=False)
