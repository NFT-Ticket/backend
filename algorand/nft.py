from algosdk.future.transaction import *
import client
from algoaccount import *
from utilities import *


# Unit name should be 8 char or less

def create_nft(nft_name, unit_name, amt, creator, manager, url):
    algod_client = client.get_algod_client()

    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()

    # Create NFT Transaction
    txn = AssetConfigTxn(
        sender=creator.public_key,
        sp=params,
        total=amt,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=nft_name,
        manager=manager.public_key,
        reserve=manager.public_key,
        freeze=manager.public_key,
        clawback=manager.public_key,
        url=url,
        decimals=0)

    # Sign with secret key of creator
    signed_txn = txn.sign(creator.secret_key)

    # Send the transaction to the network and retrieve the txid.
    try:
        txn_id = algod_client.send_transaction(signed_txn)
        print("Signed transaction with txID: {}".format(txn_id))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txn_id, 4)
        print("TXID: ", txn_id)
        print("Result confirmed in round: {}".format(
            confirmed_txn['confirmed-round']))

    except Exception as err:
        print(err)

    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))

    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txn_id)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, creator.public_key, asset_id)
        print_asset_holding(algod_client, creator.public_key, asset_id)

    except Exception as e:
        print(e)

    return asset_id


def transfer_nft(sender, receiver, asset_id):
    algod_client = client.get_algod_client()
    # TRANSFER ASSET
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    txn = AssetTransferTxn(
        sender=sender.public_key,
        sp=params,
        receiver=receiver.public_key,
        amt=10,
        index=asset_id)
    stxn = txn.sign(sender.private_key)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(
            confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
    # The balance should now be 10.
    print_asset_holding(algod_client, receiver.public_key, asset_id)
    return txid

# nft_name = "Roshan"
# amt = 1
# pk = "V7WASWYSD7AEVPM6H46SWZB25CR7LQ5C275RE2VBCHSC7NU7FRRBKKHJK4"
# sk = "K9Cd233ad3xb6rF9Z82vjluJvmujulFAeA9m8D0UPQSv7AlbEh/ASr2ePz0rZDroo/XDotf7EmqhEeQvtp8sYg=="
# creator = AlgorandAccount(pk, sk)
# create_nft(nft_name, amt, creator, creator)
# asset_id = "84222697"
