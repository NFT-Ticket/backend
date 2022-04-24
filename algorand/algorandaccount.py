from algosdk import account, mnemonic


class AlgorandAccount:
    """Represents a private key and address for an Algorand account"""

    def __init__(self, private_key):
        self.secret_key = private_key
        self.public_key = account.address_from_private_key(private_key)

    def getAddress(self) -> str:
        return self.public_key

    def getPrivateKey(self) -> str:
        return self.secret_key

    def getMnemonic(self) -> str:
        return mnemonic.from_private_key(self.secret_key)

    def __str__(self) -> str:
        return self.public_key

    @classmethod
    def FromMnemonic(cls, m: str) -> "AlgorandAccount":
        return cls(mnemonic.to_private_key(m))
