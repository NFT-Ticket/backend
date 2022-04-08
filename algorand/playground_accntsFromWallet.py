def getAllAccts(name, pw):
    from auction.testing.setup import getKmdClient
    from auction.account import Account

    kmd = getKmdClient()

    wallets = kmd.list_wallets()
    for wallet in wallets:
        kmdAccounts = []
        if wallet["name"] == name:
            print(wallet)
            walletID = wallet["id"]

            walletHandle = kmd.init_wallet_handle(walletID, pw)
            try:
                addresses = kmd.list_keys(walletHandle)
                privateKeys = [
                    kmd.export_key(walletHandle, pw, addr)
                    for addr in addresses
                ]
                kmdAccounts = [Account(sk) for sk in privateKeys]
            finally:
                kmd.release_wallet_handle(walletHandle)

        for acnt in kmdAccounts:
            print(acnt.getAddress())


getAllAccts("unencrypted-default-wallet", "")
getAllAccts("MyTestWallet1", "testpassword")
getAllAccts("MyTestWallet2", "testpassword")
