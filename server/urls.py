from django.contrib import admin
from django.urls import path
from Server import views

urlpatterns = [
    path('user/', views.user_list),
    path(r'user/<str:user_id>/', views.user),
]
