from django.contrib import admin
from django.urls import path
from Server import views

urlpatterns = [
    path("user/", views.user_list),
    path(r"user/<str:user_id>/", views.user),
    path("register-user/", views.register_user),

    path("event/", views.event_list),
    path(r"event/<str:event_id>/", views.event),
    path("register-event/", views.register_event),

    path(r"user_ticket/<str:user_id>/", views.user_ticket),
    path(r"ticket/<str:ticket_id>/", views.ticket),
]
