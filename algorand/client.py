from algosdk.v2client import algod
import os
from dotenv import load_dotenv

load_dotenv()


def get_algod_client():
    '''
    Connects to the algorand test network using purestake api
    returns the algod_client for communication with the node
    '''
    algod_address = os.getenv("algodURL")
    algod_token = os.getenv("algodToken")
    headers = {
        "X-API-Key": algod_token,
    }
    algod_client = algod.AlgodClient(algod_token, algod_address, headers)
    return algod_client
