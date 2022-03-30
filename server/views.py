from Server.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Server.serializer import *



@api_view(['GET'])
def user_list(request):
    users = User.objects.all() #complex data type
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
    