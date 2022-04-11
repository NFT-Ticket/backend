import json

from algosdk.v2client.indexer import IndexerClient

####################
INDEXER_ADDRESS = "http://localhost:8980"
INDEXER_TOKEN = ""

indexercl = IndexerClient(INDEXER_TOKEN, INDEXER_ADDRESS)
####################

with open("dump_all.json", "w") as f:
    json.dump(indexercl.accounts(), f, indent=4)
