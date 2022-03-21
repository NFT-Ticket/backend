import os

import mongoengine
from bson import ObjectId
from dotenv import load_dotenv
from mongoengine import *


def setup():
    load_dotenv()

    db_name = os.getenv("db")
    hostname = os.getenv("dbHost")
    username = os.getenv("dbUser")
    pwd = os.getenv("dbPass")

    mongoengine.connect(db=db_name, host=hostname, username=username, password=pwd)
    # mongoengine.connect(db=db_name, host="localhost:8070")


class User(Document):
    id = ObjectIdField(required=True, default=ObjectId,
                       unique=True, primary_key=True)
    username = StringField(required=True)
    password = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True)
    type = IntField(required=True)
    wallet_hash = StringField(required=True)


class EventGeo(EmbeddedDocument):
    name = StringField(required=True)
    location_name = StringField(required=True)
    address = StringField(required=True)
    city = StringField()
    state = StringField()
    dateTime = DateTimeField(required=True)

    lat_long = PointField()  # TODO: Prolly best used with google maps integration


class Event(Document):
    id = ObjectIdField(required=True, default=ObjectId,
                       unique=True, primary_key=True)
    vendor_id = ReferenceField(User, reverse_delete_rule=CASCADE)
    geo = EmbeddedDocumentField(EventGeo, required=True)
    age_restriction = BooleanField()
    images = ListField(ImageField)
    tickets_remaining = IntField()


class Ticket(Document):
    # TODO: Determine if the primary key is a combination (hash, id) or just (hash)
    hash = StringField(required=True)  # TODO: Whatever the NFT hash is
    id = ReferenceField(Event, reverse_delete_rule=CASCADE)
    seat = StringField()
    wallet_hash = ReferenceField(User, required=True)  # TODO: Consider a LazyReferenceField
    price = IntField(required=True)
    sale = BooleanField(required=True)
