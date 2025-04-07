import requests
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HttpClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*"
        })

    def post(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data, verify=False)
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, verify=False)
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
