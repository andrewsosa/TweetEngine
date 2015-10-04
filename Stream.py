# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Other libs
import json, threading

# Variables that contains the user credentials to access Twitter API
access_token = "472058940-Krvbmk4h58PPAwjqnhbgOwmBsIUVrJp3L1fGGq5o"
access_token_secret = "wdPMhCxc8jj3uWkVwDAwlVTCYG6kvFJuWn2bqP08g1OCi"
consumer_key = "DhqgE1tnvTH1KJDNPhkSkzDRZ"
consumer_secret = "Frc9EA7PROJD366dGHj89JZPqqiqlwStK0yAqFoNnbxUsrdn9Y"

# Tweet Count since beginning
tweet_count = 0
tweet_rate_recent = 0
tweet_rate_total = 0

# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            print json_data['created_at'] + " " + json_data['text']
        except:
            print "Data " + str(data)

        tweet_count = tweet_count + 1

        return True

    def on_error(self, status):
        print "Error " + str(status)
        if status == 420:
            print("420 error.")
            return False


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # Start streaming with right parameters
    tallahassee=[-85,30,-84,31]
    stream.filter(locations=tallahassee, async=true)
