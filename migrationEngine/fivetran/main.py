import requests
from requests.auth import HTTPBasicAuth
import json,os,configparser
import colorama,time
from colorama import Fore

from connectionManagers.mySQLConnectionManager import MySQLConnectionManager
from datetime import datetime



def dropTables(tables,targetServerhost,targetServerusername,targetServerpassword,targetServerdatabase,targetServerdatabaseType):
    
    if targetServerdatabaseType == "mysql":
        connectionManager = MySQLConnectionManager(targetServerhost,targetServerdatabase,targetServerusername,targetServerpassword)
    try:
        connectionManager.connect()
        connectionManager.deleteTables(tables)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        if connectionManager is not None:
            connectionManager.close()


def atlas(method, endpoint, payload=None):
    
    # Base URL for the Fivetran API
    base_url = 'https://api.fivetran.com/v1'
    
    # Set up headers with authorization
    h = {
        'Authorization': f'Bearer {api_key}:{api_secret}'
    }
    # Construct full URL
    url = f'{base_url}/{endpoint}'

    try:
        # Make the request using the specified method
        # If method is not one of the expected values, raise a ValueError
        # If the request fails for any reason, catch the exception and print an error message
        # If the HTTP status code indicates an error, raise an exception
        # If the request is successful, return the JSON response
        
        if method == 'GET':
            response = requests.get(url, headers=h, auth=a)
        elif method == 'POST':
            response = requests.post(url, headers=h, json=payload, auth=a)
        elif method == 'PATCH':
            response = requests.patch(url, headers=h, json=payload, auth=a)
        elif method == 'DELETE':
            response = requests.delete(url, headers=h, auth=a)
        else:
            raise ValueError('Invalid request method.')

        response.raise_for_status()  # Raise exception

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return None
def setScheduleType(type,connector_id):
    method = 'PATCH'  #'POST' 'PATCH' 'GET'
    endpoint = 'connectors/' + connector_id 

    payload = {
  "schedule_type": type
}

    response = atlas(method, endpoint, payload)
    
    if response is not None:
        print(Fore.CYAN + 'Call: ' + method + ' ' + endpoint + ' ' + str(payload))
        print(Fore.GREEN +  'Response: ' + response['code'])
        print(Fore.MAGENTA + str(response))

def getSuccededAt(connector_id):
    method = 'GET'  #'POST' 'PATCH' 'GET'
    endpoint = 'connectors/' + connector_id 

    payload = {}

    response = atlas(method, endpoint, payload)
    
    if response is not None:
        sTime = response['data']['succeeded_at']
        if sTime is not None:
            dt_object = datetime.fromisoformat(sTime[:-1])  # Strip 'Z' at the end as it indicates UTC timezone
            unix_timestamp = dt_object.timestamp()
            return unix_timestamp
    return 0

def getFailedAt(connector_id):
    method = 'GET'  #'POST' 'PATCH' 'GET'
    endpoint = 'connectors/' + connector_id 

    payload = {}

    response = atlas(method, endpoint, payload)
    
    if response is not None:
        fTime = response['data']['failed_at']
        if fTime is not None :
            dt_object = datetime.fromisoformat(fTime[:-1])  # Strip 'Z' at the end as it indicates UTC timezone
            unix_timestamp = dt_object.timestamp()
            return unix_timestamp    
    return 0

def waitFor(wantedState):
    state = ""
    while state != wantedState:
        time.sleep(time_to_wait_beforeRequest)
        method = 'GET'  #'POST' 'PATCH' 'GET'
        endpoint = 'connectors/' + connector_id 

        payload = {}

        response = atlas(method, endpoint, payload)
        
        if response is not None:
            state = response['data']['status']['sync_state'] 

        print(f"waiting for {wantedState} state ...")


    
def runSync():

    method = 'POST'  #'POST' 'PATCH' 'GET'
    endpoint = 'connectors/' + connector_id + '/resync'
    payload = {
        "scope":{
        schema : tables
    }
    }

    response = atlas(method, endpoint, payload)

    if response is not None:
        print(Fore.CYAN + 'Call: ' + method + ' ' + endpoint + ' ' + str(payload))
        print(Fore.GREEN +  'Response: ' + response['code'])
        print(Fore.MAGENTA + str(response))

    waitFor("syncing")
    waitFor("scheduled")

    print("syncing is done ! ")


# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

config = configparser.ConfigParser()
config.comment_prefixes = (';',)  # Set the prefix character for comments
config.read('configs/migrationEngineConfig.ini')


targetServerhost = config.get('targetServer', 'host')
targetServerusername = config.get('targetServer', 'username')
targetServerpassword = config.get('targetServer', 'password')
targetServerdatabase = config.get('targetServer', 'database')
targetServerdatabaseType = config.get('targetServer', 'databaseType')



api_key = config.get('migrationEnvironment', 'API_KEY')
api_secret = config.get('migrationEnvironment', 'API_SECRET')
connector_id = config.get('migrationEnvironment', 'connector_id')
group_id = config.get('migrationEnvironment', 'group_id')
schema = config.get('migrationEnvironment', 'schema')
time_to_wait_beforeRequest = config.getint('migrationEnvironment', 'time_to_wait_beforeRequest')

if time_to_wait_beforeRequest is None:
    time_to_wait_beforeRequest = 1

tables =  config.get('experiment', 'tables').split("+")
a = HTTPBasicAuth(api_key, api_secret)

dropTables(tables,targetServerhost,targetServerusername,targetServerpassword,targetServerdatabase,targetServerdatabaseType)    
setScheduleType("manual",connector_id)
fTime = getFailedAt(connector_id)
sTime = getSuccededAt(connector_id)
runSync()
time.sleep(time_to_wait_beforeRequest)
newFTime = getFailedAt(connector_id)
newSTime = getSuccededAt(connector_id)

if fTime == newFTime and newSTime > sTime:
    print("Experiment Succeeded !")
elif sTime == newSTime and newFTime > fTime:
    print("Experiment Failed! ")
else:
    print("check Dashboard, Experiment probably canceled !")