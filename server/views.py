from urllib import response
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
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    except Exception as e:
        return Response({"Server Exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    except Exception as e:
        return Response({"Server Exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ api_view(["GET", "POST"])
def event(request):
    if request.method == 'GET':
        print("\n\nInside get method\n")
        today = datetime.today()
        events = Event.objects.filter(
            date__gte=today, time__gte=today)  # Only unexpired events
        print(events)
        print("\n\n\n\n")
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Extract user_name, find wallet and create NFT
        try:
            user_email = request.data["vendor"]
            user = User.objects.get(email__exact=user_email)
            creator = AlgorandAccount(user.private_key)
            event_title = request.data["title"]
            nft_name = event_title[:32]
            unit_name = event_title[:8]
            amt = request.data["ticket_quantity"]
            nft_id = nft.create_nft(nft_name, unit_name, amt, creator)
        except Exception as e:
            return Response({"Server Exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            # Try to create NFT
            try:
                user_email = request.data["vendor"]
                user = User.objects.get(email__exact=user_email)
                creator = AlgorandAccount(user.private_key)
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
    try:
        event = Event.objects.get(pk=event_id)
        serializer = EventSerializer(event)
    except Event.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
