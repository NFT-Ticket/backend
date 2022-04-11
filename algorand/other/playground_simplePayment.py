from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from auction.testing.resources import *
from algosdk.mnemonic import *
from auction.util import *
from algosdk.future.transaction import *
import algosdk.account as account

####################
ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
KMD_ADDRESS = "http://localhost:4002"
KMD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
INDEXER_ADDRESS = "http://localhost:8980"
INDEXER_TOKEN = ""
# create a kmd client
client = AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
kcl = KMDClient(KMD_TOKEN, KMD_ADDRESS)
indexercl = IndexerClient(INDEXER_TOKEN, INDEXER_ADDRESS)

accnt1 = Account(account.generate_account()[0])
accnt2 = Account(account.generate_account()[0])

fundAccount(client, accnt1.getAddress(), 201000)  # This is the min total balance required for 1 party assuming the other party has no algos.
print("Before fund transfers")
print(f"Accnt1: {accnt1.getAddress()}, {getBalances(client, accnt1.getAddress())}")
print(f"Accnt2: {accnt2.getAddress()}, {getBalances(client, accnt2.getAddress())}")

unsigned_paymentTxn = PaymentTxn(accnt1.getAddress(), client.suggested_params(), accnt2.getAddress(), 100000)
signed_paymentTxn = unsigned_paymentTxn.sign(accnt1.getPrivateKey())

waitForTransaction(client, client.send_transaction(signed_paymentTxn))

print("After fund transfers")
print(f"Accnt1: {accnt1.getAddress()}, {getBalances(client, accnt1.getAddress())}")
print(f"Accnt2: {accnt2.getAddress()}, {getBalances(client, accnt2.getAddress())}")
