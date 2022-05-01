from algosdk import account, mnemonic
from security import manager


class AlgorandAccount:
    """Represents a private key and address for an Algorand account"""

    def __init__(self, encrypted_private_key):
        self.encrypted_private_key = encrypted_private_key
        self.secret_key = manager.decrypt(encrypted_private_key)
        self.public_key = account.address_from_private_key(self.secret_key)

    def get_address(self) -> str:
        return self.public_key

    def get_private_key(self) -> str:
        return self.secret_key

    def get_encrypted_private_key(self) -> str:
        return self.encrypted_private_key

    def get_mnemonic(self) -> str:
        return mnemonic.from_private_key(self.secret_key)

    def __str__(self) -> str:
        return self.public_key

    @ classmethod
    def from_mnemonic(cls, m: str) -> "AlgorandAccount":
        return cls(mnemonic.to_private_key(m))
