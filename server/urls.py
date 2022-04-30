from django.contrib import admin
from django.urls import path
from server import views

urlpatterns = [
    path(r"user/", views.user),
    path(r"user/<str:email_id>/", views.user_with_id),
    path(r"user/balance/<str:email_id>/", views.user_balance),
    path(r"user/nft/<str:email_id>/", views.nft_owned),
    path(r"user/ticket/<str:email_id>/", views.ticket_with_user_id),
    path(r"user/transaction/<str:email_id>/", views.transactions_with_user_id),

    path("event/", views.event),
    path(r"event/<str:event_id>/", views.event_with_id),
    path(r"event/ticket/<str:event_id>/", views.event_tickets),


    path(r"ticket/", views.ticket),
    path(r"ticket/<str:ticket_id>/", views.ticket_with_id),

    path(r"email/", views.get_emails),
    path(r"username/", views.get_usernames),
]
