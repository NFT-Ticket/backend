from algosdk import account, mnemonic
from . import algorandaccount
from .client import Client

# Just a random account for testing purposes
my_address = "V7WASWYSD7AEVPM6H46SWZB25CR7LQ5C275RE2VBCHSC7NU7FRRBKKHJK4"
my_private = "K9Cd233ad3xb6rF9Z82vjluJvmujulFAeA9m8D0UPQSv7AlbEh/ASr2ePz0rZDroo/XDotf7EmqhEeQvtp8sYg=="

# Second account
public = "G75SW7GOF3RXEOIERPRX3KBSZ4KC47VPJFVOYZHB5AOKJWV3SPWEE7F7YA"
private = "XXeEorfCRbDNVsa7g23CEjSmwoN3NFlAO+6xxtSzrvI3+yt8zi7jcjkEi+N9qDLPFC5+r0lq7GTh6Byk2ruT7A=="


def generate_algorand_keypair():
    '''
    Connects to the algorand sdk and creates a key pair
    Each address initally holds 0 ALGOS and can be loaded with test ALGOS
    using the Faucet @ https://bank.testnet.algorand.network/
    returns a dictionary of private_key, address key-value pairs
    '''
    private_key, address = account.generate_account()
    acc_mnemonic = mnemonic.from_private_key(private_key)
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(acc_mnemonic))
    return algorandaccount.AlgorandAccount(private_key)


def check_balance(address):
    '''
    Takes address input and returns the balance of that address in microalgos
    The balance returned might be in Test or Main net depending on which network the
    algod_client is connected to
    '''
    algod_client = Client.get_algod_client()
    account_info = algod_client.account_info(address)
    micro_algos = account_info.get('amount')
    print("Account balance: {} microAlgos".format(
        account_info.get('amount')) + "\n")
    return micro_algos


def check_assets(address):
    '''
    Takes address input and returns a list of NFT objects owned by the account holder
    The balance returned might be in Test or Main net depending on which network the
    algod_client is connected to
    NFT object is of form: {'amount': 1, 'asset-id': 84222697, 'is-frozen': False}
    '''
    algod_client = Client.get_algod_client()
    account_info = algod_client.account_info(address)
    asset_list = account_info['assets']
    return asset_list
