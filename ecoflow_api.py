def fetch_data(sn, app_key, secret_key) -> dict:
    import requests
    import json

    url = 'https://api.ecoflow.com/iot-service/open/api/device/queryDeviceQuota?sn={}'.format(sn)
    headers = {
        "Content-Type": "application/json",
        "appKey": app_key,
        "secretKey": secret_key
    }
    try:
        response_data = requests.get(url, headers=headers).text
        response_data = json.loads(response_data)
    except requests.RequestException as e:
        print(e)
        exit(1)
    return response_data
