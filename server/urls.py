from django.contrib import admin
from django.urls import path
from server import views

urlpatterns = [
    path("user/", views.user_list),
    path(r"user/<str:user_id>/", views.user),
    path("register_user/", views.register_user),
    path(r"modify_user/<str:user_id>/", views.modify_user),

    path("event/", views.event_list),
    path(r"event/<str:event_id>/", views.event),
    path("register_event/", views.register_event),
    path(r"modify_event/<str:event_id>/", views.modify_event),

    path(r"user_ticket/<str:user_id>/", views.user_ticket),
    path(r"ticket/<str:ticket_id>/", views.ticket),
    path(r"event_ticket/<str:event_id>/", views.event_ticket),

    path(r"email", views.get_emails),
    path(r"username", views.get_usernames),

]
