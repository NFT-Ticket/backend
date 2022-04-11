import json

from algosdk import account, mnemonic


def extract_account_from_mnemonic(mne):
    print(json.dumps(account.address_from_private_key(mnemonic.to_private_key(mne)), indent=4))


# extract_account_from_mnemonic("")

# ('IpKVSqPTlsa9X+JDc9vJ8XPblmlk4QkC6N92btGiRx/m3W6PwD5IlYg7WRY9EzIefRPxZBIUSyu7Ct12iKBgqw==', '43OW5D6AHZEJLCB3LELD2EZSDZ6RH4LECIKEWK53BLOXNCFAMCV4TLMRAA')
mne1 = "dust film pipe demand color immune worth time half horse top disease report grant cash thumb donkey parade husband trash people trim when abandon gun"
extract_account_from_mnemonic(mne1)
