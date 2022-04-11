import algosdk.account as account
import algosdk.mnemonic as mnemonic

accnt1 = account.generate_account()
print(accnt1)
mnemonic1 = mnemonic.from_private_key(accnt1[0])
print(mnemonic1)
