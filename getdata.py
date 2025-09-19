import requests

#### MCSERVER FUNCTION
def getdata(address):
    response = requests.get(f'https://api.mcstatus.io/v2/status/java/{address}')
    responseJson = response.json()

    if 'icon' in responseJson:
        del responseJson['icon']

    if 'motd' in responseJson:
        del responseJson['motd']

    if 'name_html' in 'version' in responseJson:
        del responseJson['version']['name_html']

    if 'list' in 'players' in responseJson:
        del responseJson['players']['list']
        
    return responseJson

def getdolar():
    response = requests.get(f'https://dolarapi.com/v1/dolares/oficial')
    responseJson = response.json()
    return responseJson

def getblue():
    response = requests.get(f'https://dolarapi.com/v1/dolares/blue')
    responseJson = response.json()
    return responseJson

def geteuro():
    response = requests.get(f'https://dolarapi.com/v1/cotizaciones/eur')
    responseJson = response.json()
    return responseJson