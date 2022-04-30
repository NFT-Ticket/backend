from algorand.algorandaccount import AlgorandAccount
from server.models import *
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view
from rest_framework import status
from server.serializer import *
from datetime import datetime
from algorand import account, nft
from django.db.models import Q


@ api_view(["GET", "POST"])
def event(request):
    '''
    GET returns a list of event objects that have not expired
    POST creates an event object in the database and also mints a NFT
        of given amount associated with the event
    '''
    if request.method == 'GET':
        today = datetime.today()
        events = Event.objects.filter(
            date__gte=today)  # Only events in the future
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Before trying to create NFT, ensure the request has valid params
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            # Try to create NFT
            try:
                user_email = request.data["vendor"]
                user = User.objects.get(email__exact=user_email)
                creator = AlgorandAccount(user.private_key)
                # Check if the minimum balance is met: 1000 Micro algos
                if account.check_balance(creator.public_key) < 1000:
                    return Response({"error": "Insufficient user balance. Use https://bank.testnet.algorand.network/ to reload your account"}, status=status.HTTP_400_BAD_REQUEST)
                event_title = request.data["title"]
                nft_name = event_title[:32]
                unit_name = event_title[:8]
                amt = request.data["ticket_quantity"]
                nft_id = nft.create_nft(nft_name, unit_name, amt, creator)
            # If NFT creation fails, don't save event data and return server error
            except Exception as e:
                return Response({"Server Exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # If no exception occurs and NFT is created, save nft_id to db along with event details
            serializer.save(tickets_remaining=amt, ticket_nft_id=nft_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(["GET", "PUT"])
def event_with_id(request, event_id):
    '''
    GET returns the event object with given event_id
    PUT modifies the event object in the db with given event_id
    '''
    try:
        event = Event.objects.get(pk=event_id)
        serializer = EventSerializer(event)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(["GET"])
def event_tickets(request, event_id):
    '''
    Returns a list of secondary tickets available for sale for given event_id
    '''
    try:
        tickets = Ticket.objects.filter(event=event_id, on_sale=True)
        serializer = TicketSerializer(tickets, many=True)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(["GET"])
@parser_classes([JSONParser])
def event_search(request):
    '''
    Searches the database for the given query and returns a list of matching event objects
    Search is performed in description, title, street_address, and city columns of the event table
    Search is performed with SQL LIKE %% query instead of an exact query match
    '''
    try:
        query = request.GET.get('query')
        events = Event.objects.filter(description__icontains=query)
        events = Event.objects.filter(
            Q(description__icontains=query) | Q(title__icontains=query) |
            Q(street_address__icontains=query) | Q(city__icontains=query))
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
