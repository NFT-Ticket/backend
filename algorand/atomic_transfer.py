from .client import Client
from algosdk.future.transaction import *
from .nft import *


def transfer_atomically(algo_transfer_txn, asset_transfer_txn, algo_sender, nft_sender):
    '''
    Takes two transactions, one of type ALGO transfer, other of type NFT transfer,
    groups the transactions as a batch and tries to atomically perform both transactions
    If either of the transaction fails, the whole transaction fails
    Returns True if both transfers successful, False otherwise
    '''
    algod_client = Client.get_algod_client()
    algo_transfer_txn_id = algo_transfer_txn.get_txid()
    asset_transfer_txn_id = asset_transfer_txn.get_txid()
    print(f"Recieved algo_transfer_txn with tx id: {algo_transfer_txn_id}")
    print(f"Received nft_transfer_txn with tx id: {asset_transfer_txn_id}")

    print("Grouping transactions...")
    # compute group id and put it into each transaction
    group_id = transaction.calculate_group_id(
        [algo_transfer_txn, asset_transfer_txn])
    print("...computed groupId: ", group_id)
    algo_transfer_txn.group = group_id
    asset_transfer_txn.group = group_id

    # sign transactions
    print("Signing transactions...")
    signed_algo_transfer_txn = algo_transfer_txn.sign(algo_sender.secret_key)
    print("...Algo Sender signed algo_transfer_txn with id: ",
          algo_transfer_txn.get_txid())
    signed_asset_transfer_txn = asset_transfer_txn.sign(nft_sender.secret_key)
    print("...NFT Sender signed nft_transfer_txn with id: ",
          asset_transfer_txn.get_txid())

    # assemble transaction group
    print("Assembling transaction group...")
    signedGroup = []
    signedGroup.append(signed_algo_transfer_txn)
    signedGroup.append(signed_asset_transfer_txn)

    try:
        # send transactions
        print("Sending transaction group...")
        tx_id = algod_client.send_transactions(signedGroup)

        # wait for confirmation
        confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)
        print("txID: {}".format(tx_id), " confirmed in round: {}".format(
            confirmed_txn.get("confirmed-round", 0)))
    except Exception as e:
        print(e)
        return False

    # If atomic transfer was successful, return True
    return True


def create_algo_transfer_txn(sender, receiver, micro_algos):
    '''
    Takes in the amount in micro_algos and returns an unsigned
    tranaction object for transferring the ALGOS from sender to
    receiver

    '''
    algod_client = Client.get_algod_client()
    # get node suggested parameters
    params = algod_client.suggested_params()
    # create transactions
    print("Creating transactions...")
    algo_transfer_txn = PaymentTxn(
        sender.public_key, params, receiver.public_key, micro_algos)
    print("...txn_1: from {} to {} for {} microAlgos".format(
        sender, receiver, micro_algos))
    print("...created txn_1: ", algo_transfer_txn.get_txid())
    return algo_transfer_txn


def create_asset_transfer_txn(sender, receiver, asset_id):
    '''
    Takes in an NFT asset_id and returns an unsigned transaction object
    for transfering the nft from sender to receiver

    '''
    # Receiver has to first opt into the NFT before receiving nft
    print(f"Opting into nft with id: {asset_id}")
    opt_in_to_nft(receiver, asset_id)

    # Create asset transfer txn
    algod_client = Client.get_algod_client()
    # get node suggested parameters
    params = algod_client.suggested_params()
    asset_transfer_txn = AssetTransferTxn(
        sender=sender.public_key,
        sp=params,
        receiver=receiver.public_key,
        amt=1,
        index=asset_id)
    return asset_transfer_txn
