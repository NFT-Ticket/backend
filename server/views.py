from Server.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from Server.serializer import *



@api_view(['GET'])
def user_list(request):
    users = User.objects.all() #complex data type
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def user(request, user_id):
    try:
        print(user_id)
        print(list(User.objects.all()))
        print(User.objects.get(first_name="TestFirst"))
        user = User.objects.get(first_name="TestFirst")
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except  User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    