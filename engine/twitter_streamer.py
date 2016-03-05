# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API

# My libaries
from event_manager import EventManager

# Other libs
import json, threading, datetime, random, logging

# Tokens for Firebase API
#firebase_url = 'https://tweetengine.firebaseio.com/'

LONG = 'longitude'
LAT  = 'latitude'

class TwitterStreamer(StreamListener):

    def __init__(self, credentials, node, southwest, northeast, extras):

        logging.info("Beginning TwitterStreamer init")

        StreamListener.__init__(self)

        # Lock and target location
        self.lock = threading.Lock()
        self.buckets = {}
        self.deltas = {}
        self.location = [southwest[LONG],southwest[LAT],northeast[LONG],northeast[LAT]]
        self.creds = credentials
        self.event_manager = EventManager()

        # Firebase & Control
        #self.firebase = Firebase(firebase_url)
        #self.messages = self.firebase.child("messages")
        #self.name = "Streamer"
        #self.nick = self.name
        #self.receiver = FirebaseListener(str(self.messages), self.on_command)
        #self.receiver.start()
        #self.respond(self.nick + " online!")

        # Upload handler
        self.node = node

        logging.info("TwitterStreamer init successful")

    #
    #   Threading Functiosn
    #

    # Start node
    def start(self):

        logging.info("Starting TwitterStreamer")

        # This handles Twitter authetification and the connection to Twitter Streaming API
        auth = OAuthHandler(self.creds['consumer_key'], self.creds['consumer_secret'])
        auth.set_access_token(self.creds['access_token'], self.creds['access_token_secret'])

        # 2nd parameter self serves as the StreamListener object
        self.stream = Stream(auth, self)

        logging.info("Created Stream object")

        # Start streaming with right parameters
        #self.stream.filter(locations=self.location, async=True)
        t = threading.Thread(target=self.stream.filter, kwargs={'locations':self.location, 'async':False})
        t.daemon = True
        t.start()

        logging.info("TwitterStreamer started successfully")

        return t



    #def join(self):
    #    # Wait for receiver to close
    #    self.receiver.stop()
    #    self.receiver.join()


    def stop(self):

        logging.info("Stopping TwitterStreamer")

        self.stream.disconnect()

        logging.info("TwitterStreamer stopped")

        # End chat and wrap up
        #try:
        #    self.receiver.stop()
        #except:
        #    self.respond("Receiver threw error on shutdown.")

        #self.respond("Shutting down...")

    #
    #   Data Management
    #

    def find_location(self, json):
        # Primary check
        coordinates = json['place']['bounding_box']['coordinates'][0]
        return coordinates

    def record_event(self,long,lat):

        key = str(long) + "," + str(lat)

        # If this is the first time recording for bucket, launch updater
        if key not in self.buckets:
            self.buckets[key] = self.buckets.get(key,0) + 1
            self.deltas[key] = datetime.datetime.now()
            self.post_bucket(key)
        else:
            self.buckets[key] += 1


    def post_bucket(self, key):

        #now = datetime.datetime.now()
        #period = (now - self.deltas[key]).total_seconds()
        #self.deltas[key] = now
        period = 10

        velocity = float(self.buckets[key]) / float(period)

        accel, torque = self.event_manager.record(velocity)

        x, y = [int(i) for i in key.split(',')]

        data = {
                'x': x,
                'y': y,
                'width': 1,
                'velocity':velocity,
                'acceleration':accel,
                'torque':torque
            }

        self.node.post_results(data)
        self.buckets[key] = 0

        # Rerun again later
        t = threading.Timer(10, self.post_bucket, args=(key,))
        t.daemon = True
        t.start()

    #
    #   Event-driven functions
    #

    # Runs for every tweet
    def on_status(self, status):

        logging.info("Status received!")

        json = status._json
        coords = self.find_location(json)

        # Random location within assigned region TODO improve this?
        left    = max(self.location[0], coords[0][0])
        bottom  = max(self.location[1], coords[0][1])
        right   = min(self.location[2], coords[2][0])
        top     = min(self.location[3], coords[2][1])

        #print "height range ", (coords[3][1] - coords[0][1])
        #print bottom, "max", self.location[1], coords[0][1]
        #print top, "min", self.location[3], coords[3][1]

        long = int(random.uniform(left, right))
        lat  = int(random.uniform(bottom, top))

        #print lat

        self.record_event(long,lat)

        return True

    def on_warning(self, warning):
        logging.warning(str(warning))
        return True

    # Catches errors
    def on_error(self, status):
        logging.critical("ERROR " + str(status))
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
                #self.respond("Sorry, I don't recognize that command.")
                self.log("Unrecognized command: " + text)

    #
    #   Utility functions
    #

    def respond(self, message):
        #self.messages.push({'name':self.nick, 'text':message})
        pass

if __name__ == '__main__':

    # TODO - UPDATE TO RECEIVE LOCATION VIA LAUNCHER
    southwest=[-87,24]
    northeast=[-79,32]

    streamer = TwitterStreamer(southwest, northeast)
    streamer.start()

    raw_input("space to stop")
    streamer.stop()
