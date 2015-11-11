# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API


# Unofficial REST Firebase API
from firebase import Firebase
from firebase_streaming import FirebaseListener

# Other libs
import json, threading, datetime

# Variables that contains the user credentials to access Twitter API
access_token = "***REMOVED***"
access_token_secret = "***REMOVED***"
consumer_key = "***REMOVED***"
consumer_secret = "***REMOVED***"

# Tokens for Firebase API
firebase_url = 'https://tweetengine.firebaseio.com/'

class EngineNode(StreamListener):

    def __init__(self, xy, level):

        # Tweet Metadata
        self.tweet_count = 0
        self.tweet_rate_recent = 0
        self.tweet_rate_total = 0
        self.tweet_rate_queue = []
        self.last_velocity_update = datetime.datetime.now()

        # Lock and target location
        self.lock = threading.Lock()
        self.level = level
        width = self.calcWidth(level)
        self.location = [xy[0], xy[1], xy[0] + width, xy[1] + width]

        # Firebase
        self.firebase = Firebase(firebase_url)
        self.messages = self.firebase.child("messages")
        self.name = str(self.location[0]) + "," + str(self.location[1]) + "," + str(self.level)
        self.nick = self.name
        self.firebase = self.firebase.child("locations").child(self.name)

        # Init node stats
        self.firebase.update({'x':self.location[0]})
        self.firebase.update({'y':self.location[1]})
        self.firebase.update({'level':self.level})

        # Begin listening for commands
        self.receiver = FirebaseListener(str(self.messages), self.on_command)
        self.receiver.start()

        # Signal online
        self.respond(self.nick + " online!")

        # Required by Tweet API since this is a stream listener
        self.api = API()



    # Start node
    def start(self):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth, self)

        # Start streaming with right parameters
        self.stream.filter(locations=self.location, async=True)

        # Begin the metadata threads
        self.launch_meta_threads()

        self.respond("Starting streaming!")


    def join(self):
        # Wait for receiver to close
        self.receiver.join()


    def stop(self):
        # Close the mining-related threads
        self.stream.disconnect()
        self.velocity_thread.cancel()
        self.firebase.remove()


    def close(self):
        # Try stopping before closing
        try:
            self.stop()
        except:
            pass

        # End chat and wrap up
        try:
            self.receiver.stop()
        except:
            self.respond("Receiver threw error on shutdown.")

        self.respond("Shutting down...")


    def calcWidth(self,level):
        return 1.0/pow(2, level)


    # Runs for every tweet
    def on_status(self, status):
        self.log(status._json['created_at'] + "\t" + status._json['text'].replace('\n',' '))
        self.tweet_count = self.tweet_count + 1
        return True

    def on_warning(self, warning):
        self.respond("I just got this warning, and I don't know what to do:")
        self.respond(str(warning))
        return True

    #def on_data(self, data):
    #    try:
    #        json_data = json.loads(data)
    #        print self.name + ":\t" + json_data['created_at'] + " " + json_data['text']
    #    except:
    #        print "Data " + str(data)
    #    self.tweet_count = self.tweet_count + 1
    #    return True

    # Catches errors
    def on_error(self, status):
        #print "ERROR " + str(status)
        self.log("ERROR" + str(status))
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

        #try:
        # Check if we are command target
        if tokens[0][1:] == self.name or tokens[0][1:] == self.nick:
            self.respond("You said my name!")

            # Things we can do
            if tokens[1] == "nick" and len(tokens) == 3:
                self.nick = tokens[2]

            elif tokens[1] == "bounds" or tokens[1] == "coords":
                self.respond(self.location)

            elif tokens[1] == "close" or tokens[1] == "stop":
                self.close()

            else:
                self.respond("Sorry, I don't recognize that command.")
                self.log("Unrecognized command: " + text)

        #except:
        #    print "Exception in parsing: " + text
        #    pass


    def respond(self, message):
        self.messages.push({'name':self.nick, 'text':message})


    def launch_meta_threads(self):
        self.update_velocity()

    # Handles velocity
    def update_velocity(self):
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
        #print self.name + ":\t" + "RECENT RATE: " + str(self.tweet_rate_recent) + " per second."
        self.log("RECENT RATE: " + str(self.tweet_rate_recent) + " per second.")
        #print self.name + ":\t" + "TOTAL RATE: " + str(self.tweet_rate_total) + " per second."
        self.log("TOTAL RATE: " + str(self.tweet_rate_total) + " per second.")

        # Push results to server
        self.firebase.update({'velocity':self.tweet_rate_recent})

        # Rerun again in 5 seconds
        self.velocity_thread = threading.Timer(5, self.update_velocity)
        self.velocity_thread.daemon = True
        self.velocity_thread.start()

    def log(self, message):
        print self.nick + ":\t" + message

if __name__ == '__main__':

    # TODO - UPDATE TO RECEIVE LOCATION VIA LAUNCHER
    tallahassee=[-85,30]
    level = 0

    node = EngineNode(tallahassee, level)
    node.start()

    #try:
    #    raw_input("Enter to stop \n")
    #except KeyboardInterrupt:
    #    print "Whoops! KeyboardInterrupt"

    #node.stop()
    #node.join()
