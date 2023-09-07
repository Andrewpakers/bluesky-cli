import requests
from bluesky_endpoints import endpoints

class BlueSkySession():
    def __init__(self, username, password):
        self.USERNAME = username
        self.PASSWORD = password
        self.BSKY_SERVER = "https://bsky.social"
        self.DID = ''
        self.EMAIL = ''
        self.ACCESS_TOKEN = ''
        self.REFRESH_TOKEN = ''
        self.createSession(username, password)
    def createSession(self, username, password):
        json = {"identifier": username, "password": password}
        response = self.post(self.BSKY_SERVER + endpoints['createSession'], json=json)
        response_body = response.json()
        error = response_body.get('error')
        message = response_body.get('message')
        if error:
            print(f'\nERROR: {error} MESSAGE: {message}\n')
            return response
        self.updateSelf(response_body)
    def updateSelf(self, response_body):
        self.DID = response_body.get('did')
        self.USERNAME = response_body.get('handle')
        self.EMAIL = response_body.get('email')
        self.ACCESS_TOKEN = response_body.get('accessJwt')
        self.REFRESH_TOKEN = response_body.get('refreshJwt')
    def getDetails(self):
        return {
            'did': self.DID,
            'username': self.USERNAME,
            'email': self.EMAIL,
            'access_token': self.ACCESS_TOKEN,
            'refresh_token': self.REFRESH_TOKEN
        }
    def getAccessToken(self):
        return self.ACCESS_TOKEN
    

    # create
    def post(self, url, json=None, headers=None, data=None, **kwargs):
        if headers is None:
            headers = {}
        headers['Authorization'] = f'Bearer {self.getAccessToken()}'
        response = requests.post(url, json=json, headers=headers, data=data, **kwargs)
        return response
    
    # read
    def get(self, uri, **kwargs):
        headers = {}
        headers['Authorization'] = f'Bearer {self.getAccessToken()}'
        url = self.BSKY_SERVER + uri
        response = requests.get(url, headers=headers, **kwargs)
        return response
    def getTimeline(self, limit=20, cursor="", algorithm="reverse-chronological"):
        uri = endpoints['getTimeline'] + f'?limit={limit}&cursor={cursor}&algorithm={algorithm}'
        response = self.get(uri)
        return response
    # update

    # delete