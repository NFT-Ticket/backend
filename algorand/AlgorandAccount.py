from algosdk import account, mnemonic


class AlgorandAccount:

    def __init__(self, pk, sk):
        self.private_key = sk
        self.public_key = pk
