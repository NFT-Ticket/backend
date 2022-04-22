from algosdk.v2client import algod
import os
from dotenv import load_dotenv

# Singleton class


class Client:
    _instance = None  # private global variable

    def __init__(self):
        '''
        Connects to the algorand test network using purestake api
        returns the algod_client for communication with the node
        '''
        if Client._instance != None:
            raise Exception(
                "Client is a singleton class with private constructor. Use get_algod_client() to get instance")
        else:
            load_dotenv()
            algod_address = os.getenv("algodURL")
            algod_token = os.getenv("algodToken")
            headers = {
                "X-API-Key": algod_token,
            }
            algod_client = algod.AlgodClient(
                algod_token, algod_address, headers)
            Client._instance = algod_client

    @staticmethod
    def get_algod_client():
        '''
            Returns the algod client using singleton pattern
            Only one instance of algod_client is present at all times
        '''
        if Client._instance == None:
            Client()
        return Client._instance
