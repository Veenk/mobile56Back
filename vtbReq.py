import requests

class vtbReq:

    def __init__(self, headers, payload, link):
        self.headers = headers
        self.payload = payload
        self.link = link

    def postResponse(self):
        return requests.post(self.link, headers=self.headers,
                             data=self.payload)

    def getResponse(self):
        return requests.get(self.link, headers=self.headers)
