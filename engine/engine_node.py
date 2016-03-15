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
            logging.debug(res.json()['message'])

            self.id = NODE_ID

            # Extract target
            target = res.json()['target']
            southwest = target['southwest']
            northeast = target['northeast']

            # See what extra fields we want
            extras = res.json()['extras']

            logging.debug(str(southwest))
            logging.debug(str(northeast))
            logging.debug('EXTRAS: ' + str(extras))

            # Launch TwitterStreamer with said location
            self.twitter_streamer = TwitterStreamer(self,southwest, northeast, extras)

            # We're good to go
            self.running = True

        except:
            logging.info('Failed to launch, make sure the server address is correct.')
            self.running = False

    def start(self):
        self.stream_thread = self.twitter_streamer.start()
        return self.stream_thread

    def stop(self):
        self.twitter_streamer.stop()
        self.stream_thread.join()
        self.running = False

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

        try:
            url = POST
            requests.post(url, data = data)
            logging.debug("POST " + str(data))
        except:
            logging.critical("Error uploading data, exiting...")
            self.stop()
            exit()


if __name__ == "__main__":

    # Get started
    en = EngineNode()

    # Exit if we're not ready
    if not en.running:
        exit()

    # Try to start the streaming process
    try:
        stream_thread = en.start()
    except:
        en.stop()
        exit()

    # (temp) Schedule auto shutdown
    logging.info("Scheduling auto-shutdown")
    t = threading.Timer(20, en.stop)
    t.daemon = True
    t.start()
    #t.join()

    # Hold main thread while engine is running
    while(en.running):
        pass


    logging.info("All done!")
