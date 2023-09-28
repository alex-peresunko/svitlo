import requests
import json
import logging


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
        logging.info("Got code={}, text={}".format(response_data.status_code, response_data.text))
        response_data = json.loads(response_data.text)
    except requests.RequestException as e:
        print(e)
    return response_data
