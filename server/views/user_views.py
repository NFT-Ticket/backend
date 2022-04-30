from server.models import *
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view
from rest_framework import status
from server.serializer import *
from algorand import account


@api_view(["GET", "POST"])
def user(request):
    '''
    GET returns list of user objects in the database
    POST registers a new user in the database and assigns a new algorand account to the user
    '''
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
            public_key, private_key = algo_account.get_address(), algo_account.get_eprivate_key()
            serializer.save(wallet_addr=public_key, private_key=private_key)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_with_id(request, email_id):
    '''
    GET returns the user object that matches the given email_id
    PUT modifies the user object that matches the given email_id
    DELETE deletes the user object that matches the given email_id
    '''
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
    '''
    Retuns a list of NFT objects owned by user with given email_id
    '''
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
    ''''
    Retuns the balance in micro ALGOS for user with given email_id
    '''
    try:
        user = User.objects.get(pk=email_id)
        serializer = UserSerializer(user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    wallet_addr = serializer.data['wallet_addr']
    try:
        micro_algos = account.check_balance(wallet_addr)
        return Response({'Micro_Algos': micro_algos}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Server Exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ api_view(["GET"])
@ parser_classes([JSONParser])
def get_emails(request):
    '''
    Returns a list of all emails registered in the db
    '''
    emails = User.objects.values('email')
    emails = [email["email"] for email in emails]
    return Response({"emails": emails}, status=status.HTTP_200_OK)


@ api_view(["GET"])
@ parser_classes([JSONParser])
def get_usernames(request):
    '''
    Returns a list of all usernames registered in the db
    '''
    usernames = User.objects.values('username')
    usernames = [username["username"] for username in usernames]
    return Response({"usernames": usernames}, status=status.HTTP_200_OK)


@ api_view(["GET"])
@ parser_classes([JSONParser])
def transactions_with_user_id(request, email_id):
    '''
    Returns a list of all transactions where the seller is
    the user with given email_id
    '''
    try:
        transactions = Transaction.objects.filter(seller=email_id)
        serializer = TransactionSerializer(transactions, many=True)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)
