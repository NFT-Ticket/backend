from django.urls import path
from .views import event_views, ticket_views, user_views

urlpatterns = [
    path(r"user/", user_views.user),
    path(r"user/<str:email_id>/", user_views.user_with_id),
    path(r"user/balance/<str:email_id>/", user_views.user_balance),
    path(r"user/nft/<str:email_id>/", user_views.nft_owned),
    path(r"user/ticket/<str:email_id>/", ticket_views.ticket_with_user_id),
    path(r"user/transaction/<str:email_id>/",
         user_views.transactions_with_user_id),

    path("event/", event_views.event),
    path(r"event/search/", event_views.event_search),
    path(r"event/<int:event_id>/", event_views.event_with_id),
    path(r"event/ticket/<str:event_id>/", event_views.event_tickets),


    path(r"ticket/", ticket_views.ticket),
    path(r"ticket/<str:ticket_id>/", ticket_views.ticket_with_id),
    path(r"verify/", ticket_views.verify_ticket),


    path(r"email/", user_views.get_emails),
    path(r"username/", user_views.get_usernames),
]
