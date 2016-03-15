# Standard libs
import requests, json, time, datetime, logging, os, threading

# Custom classes
from twitter_streamer import TwitterStreamer

# Configuration
from config import *


class EngineNode():

    def __init__(self):

        self.init_logger()

        try:
            # Acquire Target Location From Server
            url = CONNECT
            res = requests.post(url, data = {'message':'Hello, world!'})

            # Ackowledge connection? TODO handle failed connection
            logging.info(res.json()['message'])

            self.id = NODE_ID

            # Extract target
            target = res.json()['target']
            southwest = target['southwest']
            northeast = target['northeast']

            # See what extra fields we want
            extras = res.json()['extras']

            logging.info(str(southwest))
            logging.info(str(northeast))
            logging.info('EXTRAS: ' + str(extras))

            # Launch TwitterStreamer with said location
            self.twitter_streamer = TwitterStreamer(self,southwest, northeast, extras)

            # We're good to go
            self.ready = True

        except:
            logging.info('Failed to launch, make sure the server address is correct.')
            self.ready = False

    def start(self):
        self.stream_thread = self.twitter_streamer.start()
        return self.stream_thread

    def stop(self):
        self.twitter_streamer.stop()
        self.stream_thread.join()

    def init_logger(self):

        # Make sure we have a place to put our logs
        if not os.path.exists("./logs/"):
            os.makedirs("./logs/")

        # When do we start?
        filename = "./logs/" + datetime.datetime.now().strftime(FILE_FORMAT) + ".log"

        # set up logging to file
        logging.basicConfig(level=logging.DEBUG,
                            format=MESSAGE_FORMAT_FILE,
                            datefmt=DATE_FORMAT,
                            filename=filename,
                            filemode='w')

        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.addFilter(logging.Filter("root"))

        # set a format which is simpler for console use
        formatter = logging.Formatter(MESSAGE_FORMAT_CONSOLE,datefmt=DATE_FORMAT)

        # tell the handler to use this format
        console.setFormatter(formatter)

        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

    def post_results(self,data):

        # Add extra data fields
        data['id'] = self.id

        url = POST
        requests.post(url, data = data)
        logging.info("POST " + str(data))

if __name__ == "__main__":
    en = EngineNode()

    if not en.ready:
        exit()

    try:
        stream_thread = en.start()
    except:
        en.stop()
        exit()


    #
    # stop the object
    #

    logging.info("Scheduling auto-shutdown")

    t = threading.Timer(15, en.stop)
    t.daemon = True
    t.start()
    t.join()

    logging.info("All done!")
