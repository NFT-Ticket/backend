from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from auction.testing.resources import *
from algosdk.mnemonic import *
from auction.util import *

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

print(kcl.list_wallets())

## Anonymous Account 1
# anon_mnemonic_1 = "multiply wrong typical flavor purpose spider zoo gallery desert away enroll ancient rail spirit candy stem digital logic daring cake income stomach address able leave"
# acct1 = account.address_from_private_key(to_private_key(anon_mnemonic_1))
# print(fundAccount(client, "V7HGZ26UID2O7DIY44FD57Q2CJSWNUVNCEF2RLGKQZ5JB366ZHF5XQSKLA", 111222333))
# print(getBalances(client, acct))
# print(client.account_info(acct))
# print(indexercl.account_info(acct2))
