from rest_framework import serializers
from Server.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('_id', 'password', 'first_name', 'last_name', 'email', 'is_seller', 'wallet_hash')


class EventGeoSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventGeo
        fields=('_id', 'name', 'location_name', 'address', 'city', 'state', 'dateTime', 'lat_long')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=('_id', 'vendor_id', 'geo', 'age_restriction', 'images', 'tickets_remaining')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields=('_id', 'hash', 'seat', 'owner', 'price', 'sale')
