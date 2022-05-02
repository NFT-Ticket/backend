from algosdk.future.transaction import *
from .client import Client
from .algorandaccount import AlgorandAccount
from . import utilities
import json


# Unit name should be 8 char or less

def create_nft(nft_name, unit_name, amt, creator):
    algod_client = Client.get_algod_client()

    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()

    # Create NFT Transaction
    manager = creator
    # This should be IPFS Meta data URL
    url = "https://nfticket.com/"
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
        utilities.print_created_asset(
            algod_client, creator.public_key, asset_id)
        utilities.print_asset_holding(
            algod_client, creator.public_key, asset_id)

    except Exception as e:
        print(e)

    return asset_id


def opt_in_to_nft(receiver, asset_id):
    '''
    For a NFT to transfer from A to B, 
    B must opt in to receive the NFT
    This is done via a opt_in transaction, which
    results in the asset_id with balance 0 in B's account
    '''
    algod_client = Client.get_algod_client()
    # OPT-IN
    # Check if asset_id is in receivers's asset holdings prior
    # to opt-in
    params = algod_client.suggested_params()
    account_info = algod_client.account_info(receiver.public_key)
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break
    if not holding:
        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=receiver.public_key,
            sp=params,
            receiver=receiver.public_key,
            amt=0,
            index=asset_id)
        stxn = txn.sign(receiver.secret_key)
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
        # Now check the asset holding for that account.
        # This should now show a holding with a balance of 0.
        utilities.print_asset_holding(
            algod_client, receiver.public_key, asset_id)


def transfer_nft(sender, receiver, asset_id):
    # Receiver should OPT in to receive NFT, if not done so already
    opt_in_to_nft(sender, receiver, asset_id)
    algod_client = Client.get_algod_client()
    # TRANSFER ASSET
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    txn = AssetTransferTxn(
        sender=sender.public_key,
        sp=params,
        receiver=receiver.public_key,
        amt=1,
        index=asset_id)
    stxn = txn.sign(sender. secret_key)
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
    utilities.print_asset_holding(algod_client, receiver.public_key, asset_id)
    return txid
