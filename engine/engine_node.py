# Special needs
from twitter_streamer import TwitterStreamer

# Standard libs
import requests, json, time

# Server URLS
BASE_ADDR   = "http://localhost:8080/api"
CONNECT     = BASE_ADDR + "/connect"
POST         = BASE_ADDR + "/upload"

# Twitter API Credentials
access_token = "***REMOVED***"
access_token_secret = "***REMOVED***"
consumer_key = "***REMOVED***"
consumer_secret = "***REMOVED***"

twitter_creds = {
    'access_token':access_token,
    'access_token_secret':access_token_secret,
    'consumer_key': consumer_key,
    'consumer_secret':consumer_secret
}


class EngineNode():

    def __init__(self):

        # Acquire Target Location From Server
        url = CONNECT
        res = requests.post(url, data = {'id':'Test Node'})
        print res.json()['message']

        target = res.json()['target']

        southwest = target['southwest']
        northeast = target['northeast']

        print southwest
        print northeast

        # Launch TwitterStreamer with said location
        self.twitter_streamer = TwitterStreamer(twitter_creds,self,southwest, northeast)
        self.twitter_streamer.start()

    def post_results(data):
        url = POST
        #requests.post(url, data = data)
        print "POST"
        print data


if __name__ == "__main__":
    en = EngineNode()
