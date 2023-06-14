from enum import Enum

from mongoengine import Document, StringField, BooleanField, EnumField


class WayToContact(Enum):
    EMAIL = "email"
    PHONE = "phone"


class User(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)
    phone = StringField()
    way_to_contact = EnumField(WayToContact, default=WayToContact.EMAIL)

