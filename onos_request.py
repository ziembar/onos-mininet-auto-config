# import requests

# import base64
# import json

# username = "onos"
# password = "rocks"

# def setSwitch(flow_json, deviceId):

#     flow_json = json.dumps(flow_json)

#     url = "http://localhost:8181/onos/v1/flows/of:{}".format(deviceId)

#     headers = {"Content-Type": "application/json", "Accept": "application/json"}

#     response = requests.post(url=url, headers=headers, data=flow_json, auth=('karaf', 'karaf'))
#     print(response)
    
import requests
import base64
import json

# Dane uwierzytelniające (nazwa użytkownika i hasło)
username = 'onos'
password = 'rocks'

def setSwitch(flow, deviceId):
    # Tworzenie kodu base64 z nazwy użytkownika i hasła
    auth_string = f"{username}:{password}"
    base64_auth_string = base64.b64encode(auth_string.encode()).decode()

    # Adres URL serwera ONOS
    url = f"http://localhost:8181/onos/v1/flows/{deviceId}"

    # Tworzenie obiektu Request i dodawanie nagłówka Authorization
    headers = {"Authorization": f"Basic {base64_auth_string}",
               "Content-Type": "application/json",
               "Accept": "application/json"
               }

    response = requests.post(url, json=flow, headers=headers)
    if response.status_code//100 == 2:
        return "OK"
    else:
        print(f"[ERROR] Request failed with status code {response.status_code}")
        print("[ERROR] Response:", response.text)
        return "ERROR"