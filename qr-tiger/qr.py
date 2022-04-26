import requests
import json


def generate_qr(text):

    url = "https://qrtiger.com/api/qr/static"
    key = "Bearer 0e7fc850-c500-11ec-a952-e7d3ec2d6654"

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
                "text": "https://google.com?q=" + text
            }
    payload = json.dumps(payload)
    headers = {
        'Content-Type': "application/json",
        'Authorization': key
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    res = response.json()
    qr_url = res["url"]
    return qr_url
