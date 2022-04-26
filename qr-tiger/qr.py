import requests
import json
import os
from cryptography.fernet import Fernet
import time
import base64


def generate_qr(text):

    url = "https://qrtiger.com/api/qr/static"
    apikey = "Bearer 0e7fc850-c500-11ec-a952-e7d3ec2d6654"

    encrypted_text = str(encrypt(text), "UTF-8")
    payload = {
                "size": 500,
                "colorDark": "rgb(5,64,128)",
                "logo": "scan_me.png",
                "eye_outer": "eyeOuter2",
                "eye_inner": "eyeInner1",
                "qrData": "pattern0",
                "backgroundColor": "rgb(255,255,255)",
                "transparentBkg": False,
                "qrCategory": "url",
                "text": "https://google.com?q=" + encrypted_text
            }
    payload = json.dumps(payload)
    headers = {
        'Content-Type': "application/json",
        'Authorization': apikey
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    res = response.json()
    if "url" in res:
        qr_url = res["url"]
    else:
        qr_url = None
    return qr_url


def encrypt(text):

    # Fernet key must be 32 url-safe base 64-encoded bytes
    key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456".encode('ascii')
    key = base64.b64encode(key)
    fernet = Fernet(key)

    data = {"text": text,
            "time": time.time()}
    data = json.dumps(data)

    # to encrypt the string, string must be encoded to byte string before encryption
    encrypt_data = fernet.encrypt(data.encode())

    return encrypt_data


def decrypt(text):
    
    # Fernet key must be 32 url-safe base 64-encoded bytes
    key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456".encode('ascii')
    key = base64.b64encode(key)
    fernet = Fernet(key)

    text = bytes(text, "UTF-8")

    decrypted_text = fernet.decrypt(text).decode()
    return decrypted_text
