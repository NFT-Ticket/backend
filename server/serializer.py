from rest_framework import serializers
from rest_framework_mongoengine.fields import ObjectIdField

class UserSerializer(serializers.Serializer):
    _id = ObjectIdField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    is_seller = serializers.BooleanField()
    wallet_hash = serializers.CharField()