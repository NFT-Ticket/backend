from algosdk import account, mnemonic
from .algorandaccount import AlgorandAccount
from .client import Client
from security import manager


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
    encrypted_key = manager.encrypt(private_key)
    return AlgorandAccount(encrypted_key)


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


def check_asset_ownership(address, nft_id):
    '''
    Takes in a asset id and a wallet address and returns a boolean to 
    indicate whether the user with given address owns the nft_id or not
    '''
    algod_client = Client.get_algod_client()
    account_info = algod_client.account_info(address)
    asset_list = account_info['assets']
    for asset in asset_list:
        if asset['asset-id'] == int(nft_id) and asset['amount'] > 0:
            return True
    return False
