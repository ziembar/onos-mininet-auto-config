import urllib.request as request
import base64
import json

username = "onos"
password = "rocks"

def setSwitch(flow_json, deviceId):
    flow_json = json.dumps(flow_json).encode('utf-8')

    url = "http://localhost:8181/onos/v1/flows/of:{deviceId}".format(deviceId = deviceId)
    print(url)

    myRequest = request.Request(url, data=flow_json, headers={"Content-Type": "application/json", "Accept": "application/json"})
    base64string = base64.b64encode(('%s:%s' % (username, password)).encode('utf-8')).decode('utf-8')
    myRequest.add_header("Authorization", "Basic %s" % base64string)

    try:
        response = request.urlopen(myRequest)
        if response.getcode() == 200:
            print("Request successful")
        else:
            print(f"Request failed with status code {response.getcode()}")
    except Exception as e:
        print(f"Request failed with {e}")