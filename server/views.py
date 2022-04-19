from urllib import response
from server.models import *
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view
from rest_framework import status
from server.serializer import *
from django.http import JsonResponse
from algorand import account


@api_view(["GET", "POST"])
def user(request):
    if request.method == 'GET':
        users = User.objects.all()  # complex data type
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            # creates private/public key for algorand wallet
            algo_account = account.generate_algorand_keypair()
            public_key, private_key = algo_account.public_key, algo_account.secret_key
            serializer.save(wallet_addr=public_key, private_key=private_key)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_with_id(request, email_id):
    try:
        user = User.objects.get(pk=email_id)
        serializer = UserSerializer(user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@parser_classes([JSONParser])
def nft_owned(request, email_id):
    try:
        user = User.objects.get(pk=email_id)
        serializer = UserSerializer(user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    wallet_addr = serializer.data['wallet_addr']
    try:
        nfts_owned = account.check_assets(wallet_addr)
        return Response({'NFTs owned': nfts_owned}, status=status.HTTP_200_OK)
    except Exception:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@parser_classes([JSONParser])
def user_balance(request, email_id):
    try:
        user = User.objects.get(pk=email_id)
        serializer = UserSerializer(user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    wallet_addr = serializer.data['wallet_addr']
    try:
        micro_algos = account.check_balance(wallet_addr)
        return Response({'Micro ALGOs': micro_algos}, status=status.HTTP_200_OK)
    except Exception:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(["GET"])
def event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(["POST"])
def register_event(request):
    data = request.data
    Event.objects.create(age_restriction=data['age_restriction'], tickets_remaining=data['tickets_remaining'], vendor_id=data['vendor_id'],
                         name=data['name'], description=data['description'], location_name=data[
                             'location_name'], address=data['address'], city=data['city'],
                         state=data['state'], date=data['date'], time=data['time'])
    return Response(status=status.HTTP_200_OK)


@ api_view(["GET"])
def event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@ api_view(["POST"])
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


@ api_view(["GET"])
def user_ticket(request, user_id):
    try:
        tickets = Ticket.objects.filter(owner_id=user_id)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@ api_view(["GET"])
def ticket(response, ticket_id):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    except Ticket.DoesNotExist:
        return Response(status=status.HTPP_404_NOT_FOUND)


@ api_view(["GET"])
def event_ticket(request, event_id):
    try:
        tickets = Ticket.objects.filter(event_id=event_id)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Ticket.DoesNotExist:
        return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(["GET"])
@parser_classes([JSONParser])
def get_emails(request):
    emails = User.objects.values('email')
    emails = [email["email"] for email in emails]
    return Response({"emails": emails}, status=status.HTTP_200_OK)


@ api_view(["GET"])
@parser_classes([JSONParser])
def get_usernames(request):
    usernames = User.objects.values('username')
    usernames = [username["username"] for username in usernames]
    return Response({"usernames": usernames}, status=status.HTTP_200_OK)
