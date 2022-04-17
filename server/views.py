from urllib import response
from server.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from server.serializer import *
from django.db.models import Count
from django.core import serializers
import json
from django.http import HttpResponse, JsonResponse


@api_view(["GET"])
def user_list(request):
    users = User.objects.all()  # complex data type
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def register_user(request):
    data = request.data
    User.objects.create(first_name=data['first_name'], last_name=data['last_name'],
                        email=data['email'], is_seller=data['is_seller'], wallet_hash=data['wallet_hash'])
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def user(request, user_id):
    try:
        user = User.objects.get(email=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def modify_user(request, user_id):
    try:
        user = User(id=user_id)
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.email = request.data['email']
        user.is_seller = request.data['is_seller']
        user.wallet_hash = request.data['wallet_hash']
        user.save()
        return Response(status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def register_event(request):
    data = request.data
    Event.objects.create(age_restriction=data['age_restriction'], tickets_remaining=data['tickets_remaining'], vendor_id=data['vendor_id'],
                         name=data['name'], description=data['description'], location_name=data[
                             'location_name'], address=data['address'], city=data['city'],
                         state=data['state'], date=data['date'], time=data['time'])
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def modify_event(request, event_id):
    try:
        data = request.data
        event = Event(id=event_id)
        event.age_restriction = data['age_restriction']
        event.tickets_remaining = data['tickets_remaining']
        event.name = data['name']
        event.description = data['description']
        event.location_name = data['location_name']
        event.address = data['address']
        event.city = data['city']
        event.state = data['state']
        event.date = data['date']
        event.time = data['time']
        event.vendor_id = data['vendor_id']
        event.save()
        return Response(status=status.HTTP_200_OK)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def user_ticket(request, user_id):
    try:
        tickets = Ticket.objects.filter(owner_id=user_id)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def ticket(response, ticket_id):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    except Ticket.DoesNotExist:
        return Response(status=status.HTPP_404_NOT_FOUND)


@api_view(["GET"])
def event_ticket(request, event_id):
    try:
        tickets = Ticket.objects.filter(event_id=event_id)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Ticket.DoesNotExist:
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_emails(request):
    emails = User.objects.values('email')
    emails = [email["email"] for email in emails]
    return JsonResponse(emails, safe=False)


@api_view(["GET"])
def get_usernames(request):
    # TODO: Change to username after DB change
    usernames = User.objects.values('first_name')
    usernames = [username["first_name"] for username in usernames]
    return JsonResponse(usernames, safe=False)
