from algosdk import account, mnemonic
from algosdk.v2client import algod
import os
from dotenv import load_dotenv

load_dotenv()

# Just a random account for testing purposes
my_address = "V7WASWYSD7AEVPM6H46SWZB25CR7LQ5C275RE2VBCHSC7NU7FRRBKKHJK4"
my_private = "K9Cd233ad3xb6rF9Z82vjluJvmujulFAeA9m8D0UPQSv7AlbEh/ASr2ePz0rZDroo/XDotf7EmqhEeQvtp8sYg=="


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


def generate_algorand_keypair():
    '''
    Connects to the algorand sdk and creates a key pair
    Each address initally holds 0 ALGOS and can be loaded with test ALGOS
    using the Faucet @ https://bank.testnet.algorand.network/
    returns a dictionary of private_key, address key-value pairs
    '''
    private_key, address = account.generate_account()
    # print("My address: {}".format(address))
    # print("My private key: {}".format(private_key))
    # print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    return {"private_key": private_key, "address": address}


def check_balance(address):
    '''
    Takes address input and returns the balance of that address in microalgos
    The balance returned might be in Test or Main net depending on which network the 
    algod_client is connected to
    '''
    algod_client = get_algod_client()
    account_info = algod_client.account_info(address)
    micro_algos = account_info.get('amount')
    # print("Account balance: {} microAlgos".format(
    #     account_info.get('amount')) + "\n")
    return micro_algos
