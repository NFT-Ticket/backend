from django.contrib import admin
from django.urls import path
from server import views

urlpatterns = [
    path(r"user/", views.user),
    path(r"user/<str:email_id>/", views.user_with_id),
    path(r"user/balance/<str:email_id>/", views.user_balance),
    path(r"user/nft/<str:email_id>/", views.nft_owned),

    path("event/", views.event_list),
    path(r"event/<str:event_id>/", views.event),
    path("register_event/", views.register_event),
    path(r"modify_event/<str:event_id>/", views.modify_event),

    path(r"user_ticket/<str:user_id>/", views.user_ticket),
    path(r"ticket/<str:ticket_id>/", views.ticket),
    path(r"event_ticket/<str:event_id>/", views.event_ticket),

    path(r"email/", views.get_emails),
    path(r"username/", views.get_usernames),
]
