import urllib.request
import base64

# Dane uwierzytelniające (nazwa użytkownika i hasło)
username = 'onos'
password = 'rocks'

# Tworzenie kodu base64 z nazwy użytkownika i hasła
auth_string = f"{username}:{password}"
base64_auth_string = base64.b64encode(auth_string.encode()).decode()

# Adres URL serwera ONOS
urlLinks = "http://192.168.56.104:8181/onos/v1/links"
urlDevices = "http://192.168.56.104:8181/onos/v1/devices"

# Tworzenie obiektu Request i dodawanie nagłówka Authorization
def getLinks():
    request = urllib.request.Request(urlLinks)
    request.add_header("Authorization", f"Basic {base64_auth_string}")

    # Wysyłanie zapytania GET
    response = urllib.request.urlopen(request)
    content = response.read()

    return content

def getDevices():
    request = urllib.request.Request(urlDevices)
    request.add_header("Authorization", f"Basic {base64_auth_string}")

    # Wysyłanie zapytania GET
    response = urllib.request.urlopen(request)
    content = response.read()

    return content