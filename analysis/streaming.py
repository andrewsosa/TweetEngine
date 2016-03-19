# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API

import threading

# My libaries
from config import *

counter = 0

num_Point = 0
num_Polygon = 0
num_Geo = 0
num_Large = 0
num_Small = 0

t_progress = None
margins = []

def average(x):
    return [sum(y) / len(y) for y in zip(*x)]

def progress():
    global t_progess
    print "Tweets counted: ", counter
    t_progress = threading.Timer(10, progress)
    t_progress.daemon = True
    t_progress.start()


t_progress = threading.Timer(10.0, progress)
t_progress.daemon = True


class CustomListener(StreamListener):

    def on_status(self, status):

        global counter
        global num_Point
        global num_Polygon
        global num_Geo
        global num_Large
        global num_Small

        bb = status.place.bounding_box
        cd = bb.coordinates

        if bb.type == 'Polygon':

            lng = cd[0][3][0] - cd[0][0][0]
            lat = cd[0][2][1] - cd[0][0][1]

            if lng > 0.1 or lat > 0.1:
                num_Large += 1
            else:
                num_Small += 1


            margins.append((lng,lat))
            num_Polygon += 1
        elif bb.type == 'Point':
            num_Point += 1

        if status.geo != None:
            num_Geo += 1


        if counter < 10000:
            counter += 1
            return True

        return False



auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

southwest=[-87,24]
northeast=[-79,32]

cm = CustomListener()
stream = Stream(auth, cm)

print "Started streaming"

t_progress.start()
stream.filter(locations=southwest+northeast)
t_progress.cancel()

print "Finished streaming"

print "num_Point", num_Point
print "num_Geo", num_Geo
print "num_Polygon", num_Polygon
print "num_Large", num_Large
print "num_Small", num_Small
print "average(margins)", average(margins)

with file('records.txt', 'w') as f:
    for m in margins:
        f.write("%s\n" % str(m).lstrip('(').rstrip(')'))

#
# num_Point 0
# num_Geo 1027
# num_Polygon 10001
# average(margins) [2.599943050895038, 2.279429337966205]
