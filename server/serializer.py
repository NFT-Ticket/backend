from rest_framework import serializers
from Server.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('__all__')


# class EventGeoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=EventGeo
#         fields=('__all__')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=('__all__')

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields=('__all__')