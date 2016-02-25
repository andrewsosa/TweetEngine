# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API

# Unofficial REST Firebase API
from firebase import Firebase
from firebase_streaming import FirebaseListener

# Other libs
import json, threading, datetime, random

# Variables that contains the user credentials to access Twitter API
access_token = "***REMOVED***"
access_token_secret = "***REMOVED***"
consumer_key = "***REMOVED***"
consumer_secret = "***REMOVED***"

# Tokens for Firebase API
firebase_url = 'https://tweetengine.firebaseio.com/'

class TwitterStreamer(StreamListener):

    def __init__(self, southwest, northeast):

        StreamListener.__init__(self)

        # Lock and target location
        self.lock = threading.Lock()
        self.bucket = {}
        self.location = [southwest[0],southwest[1],northeast[0],northeast[1]]

        # Firebase & Control
        self.firebase = Firebase(firebase_url)
        self.messages = self.firebase.child("messages")
        self.name = "Streamer"
        self.nick = self.name
        #self.receiver = FirebaseListener(str(self.messages), self.on_command)
        #self.receiver.start()
        #self.respond(self.nick + " online!")

    #
    #   Threading Functiosn
    #

    # Start node
    def start(self):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth, self)

        # Start streaming with right parameters
        self.stream.filter(locations=self.location, async=True)

        self.respond("Starting streaming!")


    def join(self):
        # Wait for receiver to close
        self.receiver.stop()
        self.receiver.join()


    def stop(self):
        # Close the mining-related threads
        self.stream.disconnect()
        #self.velocity_thread.cancel()
        #self.firebase.remove()

        # End chat and wrap up
        try:
            self.receiver.stop()
        except:
            self.respond("Receiver threw error on shutdown.")

        self.respond("Shutting down...")

        for key in self.bucket.keys():
            self.firebase.child("locations").child(key+",0").remove()


    #
    #   Data Management
    #

    def find_location(self, json):

        # Primary check
        coordinates = json['place']['bounding_box']['coordinates'][0]
        return coordinates

    def verify_location(self, coords):
        # This function may eventually become useful. 
        return True
        # [[x1,y1],[x1,y2],[x2,y1],[x2,y2]]
        west = coords[0][0] > self.location[0]
        south = coords[0][1] > self.location[1]
        east = coords[3][0] < self.location[2]
        north = coords[3][1] < self.location[3]
        return west and south and east and north

    def init_node(self, dbkey, long, lat):
        # Init node stats
        ref = self.firebase.child("locations").child(dbkey)
        ref.update({'x':long})
        ref.update({'y':lat})
        ref.update({'level':0})


    def do_location_updates(self, key, dbkey):

        period = 10

        ref = self.firebase.child("locations").child(dbkey)
        velocity = float(self.bucket[key]) / float(period)
        #print key + "\t" + str(velocity)
        #print key + " " + str(self.bucket[key]) + " " + str(velocity)
        ref.update({'velocity':velocity})

        self.bucket[key] = 0

        # Rerun again in 5 seconds
        t = threading.Timer(period, self.do_location_updates, args=(key, dbkey))
        t.daemon = True
        t.start()


    #
    #   Event-driven functions
    #

    # Runs for every tweet
    def on_status(self, status):

        json = status._json
        coords = self.find_location(json)

        if(self.verify_location(coords)):
            #print coords

            print json['text']


            # Random location within bounding box TODO improve this?
            long = int(random.uniform(coords[0][0], coords[3][0]))
            lat  = int(random.uniform(coords[0][1], coords[3][1]))

            # Proper storage
            key = str(long) + "," + str(lat)
            if key not in self.bucket:
                self.init_node(key+",0", long, lat)
                self.bucket[key] = self.bucket.get(key,0) + 1
                self.do_location_updates(key, key+",0") # TODO update this to a thread launch
            else:
                self.bucket[key] = self.bucket[key] + 1

        return True

    def on_warning(self, warning):
        self.respond("I just got this warning, and I don't know what to do:")
        self.respond(str(warning))
        return True

    # Catches errors
    def on_error(self, status):
        #print "ERROR " + str(status)
        self.log("ERROR " + str(status))
        #if status == 420:
        #    print("420 error.")
        return False

    # Handles incoming control signals
    def on_command(self, command):

        # Reformat incoming commands
        name = command['name']
        text = command['text']

        try:
            name = name.encode('UTF-8')
            text = text.encode('UTF-8')
        except:
            return

        # Don't act on messages we sent.
        if name == self.name:
            return

        # Attempt to parse for commands
        tokens = text.split()

        if tokens[0][1:] == self.name or tokens[0][1:] == self.nick:

            if tokens[1] == "close" or tokens[1] == "stop":
                self.close()

            else:
                self.respond("Sorry, I don't recognize that command.")
                self.log("Unrecognized command: " + text)

    def respond(self, message):
        self.messages.push({'name':self.nick, 'text':message})

    def log(self, message):
        print self.nick + ":\t" + message

if __name__ == '__main__':

    # TODO - UPDATE TO RECEIVE LOCATION VIA LAUNCHER
    southwest=[-87,24]
    northeast=[-79,32]

    streamer = TwitterStreamer(southwest, northeast)
    streamer.start()

    raw_input("space to stop")
    streamer.stop()
