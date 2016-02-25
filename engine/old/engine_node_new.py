import tweepy


# Variables that contains the user credentials to access Twitter API
access_token = "***REMOVED***"
access_token_secret = "***REMOVED***"
consumer_token = "***REMOVED***"
consumer_secret = "***REMOVED***"

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

f = file("tweets.txt", "w")

tweet_count = 0

class NodeStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        f.write(str(status))
        f.write("\n")
        global tweet_count
        tweet_count += 1

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


if __name__ == "__main__":


    NodeStreamListener = NodeStreamListener()
    myStream = tweepy.Stream(auth, NodeStreamListener)
    myStream.filter(locations=[-88,30,-80,38])

    while(tweet_count < 1001):
        continue

    myStream.disconnect()
    f.close()
