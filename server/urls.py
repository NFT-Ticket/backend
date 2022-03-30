from django.contrib import admin
from django.urls import path
from Server.views import *

urlpatterns = [
    path('/', user_list)
]
