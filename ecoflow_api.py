import requests
import json


def fetch_data(sn, app_key, secret_key) -> dict:

    url = 'https://api.ecoflow.com/iot-service/open/api/device/queryDeviceQuota?sn={}'.format(sn)
    headers = {
        "Content-Type": "application/json",
        "appKey": app_key,
        "secretKey": secret_key
    }
    response_data = None
    try:
        response_data = requests.get(url, headers=headers)
        text = response_data.text
        code = response_data.status_code
        response_data = json.loads(text)
        print("Got code={}, text={}".format(code, text))
    except requests.RequestException as e:
        print(e)
    return response_data
