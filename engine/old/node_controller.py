# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Unofficial REST Firebase API
from firebase import Firebase
from firebase_streaming import FirebaseListener

# Other libs
import json, threading, datetime

# Tokens for Firebase API
firebase_url = 'https://tweetengine.firebaseio.com/'

class NodeController(StreamListener):

    def __init__(self):

        # Lock and target location
        self.lock = threading.Lock()

        # Firebase
        self.firebase = Firebase(firebase_url)
        self.messages = self.firebase.child("messages")
        self.firebase = self.firebase.child("controller")
        self.name = "controller"
        self.nick = self.name

        # Begin listening for messages
        self.receiver = FirebaseListener(str(self.messages), self.on_command)
        self.receiver.start()

        # Signal online
        self.respond(self.nick + " online!")


    def join(self):
        pass
        # Wait for receiver to terminate
        #self.receiver.join()



    def close(self):
        self.firebase.remove()
        self.receiver.stop()
        self.respond("Shutting down...")


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

            elif tokens[1] == "stop" or tokens[1] == "close":
                self.close()

            else:
                self.respond("Sorry, I don't recognize that command.")
                print "Unrecognized command: " + text


        #except:
        #    print "Exception in parsing: " + text
        #    self.respond("Uhh, I threw a parsing exception to that command.")
        #    pass

        #print tokens


    def respond(self, message):
        self.messages.push({'name':self.nick, 'text':message})


if __name__ == '__main__':

    controller = NodeController()
    #node.start()
    #controller.join()

    #try:
    #    raw_input("Enter to stop \n")
    #except KeyboardInterrupt:
    #    print "Whoops! KeyboardInterrupt"

    #node.stop()
    #controller.close()
