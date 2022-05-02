from algorand.algorandaccount import AlgorandAccount
from server.models import *
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view
from rest_framework import status
from server.serializer import *
from algorand import account, atomic_transfer
from datetime import date
from django.shortcuts import redirect


@ api_view(["POST"])
@ parser_classes([JSONParser])
def ticket(request):
    '''
    Tries to make a purchase of an event ticket for the given buyer
    Purchase is successful if buyer has enough ALGO balance in their account and
    the atomic transfer is successful for NFT and ALGOs
    If the purchase is successful, a ticket is issued for the buyer in the tickets table
    '''
    try:
        event_id = request.data["event_id"]
        buyer_email = request.data["buyer"]
        event = Event.objects.get(pk=event_id)
        # Check if ticket is available or not
        if event.tickets_remaining == 0:
            raise Exception(
                f"No tickets remaining for event with id {event_id}")
        seller = event.vendor
        buyer = User.objects.get(pk=buyer_email)
        ticket_price = event.event_price
        # Check if buyer has enough balance in their account
        if account.check_balance(buyer.wallet_addr) < ticket_price:
            return Response({"error": "Insufficient user balance. Use https://bank.testnet.algorand.network/ to reload your account"}, status=status.HTTP_400_BAD_REQUEST)
        nft_id = event.ticket_nft_id
        # Create Algorand account objects from user objects
        buyer = AlgorandAccount(buyer.private_key)
        seller = AlgorandAccount(seller.private_key)
        # Creating unsigned algo transfer txn
        algo_transfer_txn = atomic_transfer.create_algo_transfer_txn(
            buyer, seller, ticket_price)
        # Creating unsigned NFT transfer txn
        asset_transfer_txn = atomic_transfer.create_asset_transfer_txn(
            seller, buyer, nft_id)
        # Try atomic transfer
        if atomic_transfer.transfer_atomically(algo_transfer_txn, asset_transfer_txn, buyer, seller):
            print("Atomic transfer was successful.....Now creating a ticket for the user")
            # Create the ticket to save to the buyer's account
            new_ticket = {"event": event_id,
                          "nft_id": nft_id, "owner": buyer_email,
                          "is_expired": False, "on_sale": False, "price": ticket_price}
            serializer = TicketSerializer(data=new_ticket)
            if serializer.is_valid():
                serializer.save()
                event.tickets_remaining = event.tickets_remaining - 1
                event.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Atomic transfer failed, return server error
            return Response({"error": "Atomic Transfer failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(["GET", "PUT", "PATCH"])
@ parser_classes([JSONParser])
def ticket_with_id(request, ticket_id):
    '''
    GET returns the ticket with given ticket_id
    PUT modifies the ticket with given ticket_id and is intended to be used for marking ticket on sale
    PATCH is intended to make a secondary ticket purchase and modifies the owner of the ticket and creates
        a transaction in the transaction table, all using atomic transfer
    '''
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        serializer = TicketSerializer(ticket)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        try:
            if not ticket.on_sale:
                raise Exception(
                    "Ticket not on sale by the owner, cannot make a purchase")
            buyer_email = request.data["buyer"]
            ticket_price = ticket.price
            nft_id = ticket.nft_id
            buyer_obj = User.objects.get(pk=buyer_email)
            seller_obj = ticket.owner
            # Create Algorand account objects from user objects
            buyer = AlgorandAccount(buyer_obj.private_key)
            seller = AlgorandAccount(seller_obj.private_key)
            # Check if buyer has enough balance in their account
            if account.check_balance(buyer.public_key) < ticket_price + 1000:
                return Response({"error": "Insufficient buyer balance. Use https://bank.testnet.algorand.network/ to reload your account"}, status=status.HTTP_400_BAD_REQUEST)
            # Check if seller has enough balance in their account
            if account.check_balance(seller.public_key) < 1000:
                return Response({"error": "Insufficient Seller balance. Use https://bank.testnet.algorand.network/ to reload your account"}, status=status.HTTP_400_BAD_REQUEST)
            # Creating unsigned algo transfer txn
            algo_transfer_txn = atomic_transfer.create_algo_transfer_txn(
                buyer, seller, ticket_price)
            # Creating unsigned NFT transfer txn
            asset_transfer_txn = atomic_transfer.create_asset_transfer_txn(
                seller, buyer, nft_id)
            # Try atomic transfer
            if atomic_transfer.transfer_atomically(algo_transfer_txn, asset_transfer_txn, buyer, seller):
                ticket.on_sale = False
                ticket.owner = buyer_obj
                ticket.save()
                serializer = TicketSerializer(ticket)
                transaction = {"ticket": ticket_id, "buyer": buyer_obj.email,
                               "seller": seller_obj.email, "price_sold": ticket_price, "date_sold": date.today()}
                transaction_serializer = TransactionSerializer(
                    data=transaction)
                if transaction_serializer.is_valid():
                    transaction_serializer.save()
                    return Response(transaction_serializer.data, status=status.HTTP_200_OK)
                return Response(transaction_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # Atomic transfer failed, return server error
                return Response({"error": "Atomic Transfer failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(["GET"])
@ parser_classes([JSONParser])
def ticket_with_user_id(request, email_id):
    '''
    Returns a list of tickets owned by the user with given email_id
    '''
    try:
        tickets = Ticket.objects.filter(owner=email_id)
        serializer = TicketSerializer(tickets, many=True)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)


@ api_view(["GET"])
@parser_classes([JSONParser])
def verify_ticket(request):
    '''
    Takes two query parameters: email and nftid and searches the 
    algorand blockchain if user with given email owns the given nftid or not
    redirects to success or failure page based on input query
    '''
    try:
        email = request.GET.get('owner')
        nft_id = request.GET.get('nftid')
        user = User.objects.get(pk=email)
        wallet = user.wallet_addr
        # If user owns the nft, redirect to valid ticket
        if account.check_asset_ownership(wallet, nft_id):
            response = redirect('/success/')
            return response
        else:
            response = redirect('/failure/')
            return response
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
