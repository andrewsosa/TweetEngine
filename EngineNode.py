# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Other libs
import json, threading, datetime

# Variables that contains the user credentials to access Twitter API
access_token = "***REMOVED***"
access_token_secret = "***REMOVED***"
consumer_key = "***REMOVED***"
consumer_secret = "***REMOVED***"

class EngineNode(StreamListener):

    def __init__(self, location):

        # Tweet Metadata
        self.tweet_count = 0
        self.tweet_rate_recent = 0
        self.tweet_rate_total = 0
        self.tweet_rate_queue = []
        self.last_velocity_update = datetime.datetime.now()

        # Lock and target location
        self.lock = threading.Lock()
        self.location = location

    # Start node
    def start(self):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth, self)

        # Start streaming with right parameters
        self.stream.filter(locations=self.location, async=True)

        # Begin the velocity thread
        self.updateVelocity()

        # Listen for exit
        raw_input("Press ENTER to exit...")
        self.stream.disconnect()


    # Runs for every tweet
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            print json_data['created_at'] + " " + json_data['text']
        except:
            print "Data " + str(data)
        self.tweet_count = self.tweet_count + 1
        return True

    # Catches errors
    def on_error(self, status):
        print "Error " + str(status)
        if status == 420:
            print("420 error.")
            return False

    # Handles velocity
    def updateVelocity(self):
        temp = self.last_velocity_update

        # Extract lockable resources, reset counter
        self.lock.acquire()
        t_count = self.tweet_count
        self.tweet_count = 0
        self.last_velocity_update = datetime.datetime.now()
        self.lock.release()

        # Handle average updating
        diff = (self.last_velocity_update - temp).total_seconds()
        if diff != 0:
            self.tweet_rate_recent = t_count / diff

        # Handle approximate total velocity
        self.tweet_rate_queue.append(self.tweet_rate_recent)
        if len(self.tweet_rate_queue) > 1024:
            self.tweet_rate_queue.pop(0)
        self.tweet_rate_total = sum(self.tweet_rate_queue) / len(self.tweet_rate_queue)

        # Print results
        print "RECENT RATE: " + str(self.tweet_rate_recent) + " per second."
        print "TOTAL RATE: " + str(self.tweet_rate_total) + " per second."

        # Rerun again in 15 seconds
        t = threading.Timer(15, self.updateVelocity)
        t.daemon = True
        t.start()

if __name__ == '__main__':

    # TODO - UPDATE TO RECEIVE LOCATION VIA LAUNCHER
    tallahassee=[-85,30,-84,31]

    node = EngineNode(tallahassee)
    node.start()
