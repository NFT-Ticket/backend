from algosdk.future.transaction import *
import client
import json


#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break


#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


def create_nft(nft_name, amt, creator, manager):
    algod_client = client.get_algod_client()

    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()

    # Create NFT Transaction
    txn = AssetConfigTxn(
        sender=creator.public_key,
        sp=params,
        total=amt,
        default_frozen=False,
        unit_name=nft_name,
        asset_name=nft_name,
        manager=manager.public_key,
        reserve="",
        freeze="",
        clawback="",
        url="https://iamroshanpoudel.com",
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
