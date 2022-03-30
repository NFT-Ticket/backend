from Server.models import *
from django.http import JsonResponse

# Create your views here.


def user_list(request):
    users = User.objects.all() #complex data type
    user_list = list(users.values())
    return JsonResponse({
        "users": user_list
    })
    