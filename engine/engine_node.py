# Special needs
from twitter_streamer import TwitterStreamer

# Standard libs
import requests, json, time, datetime, logging, os, threading

# Server URLS
BASE_ADDR   = "http://localhost:8080/api"
CONNECT     = BASE_ADDR + "/connect"
POST        = BASE_ADDR + "/upload"

# Twitter API Credentials
access_token = "472058940-Krvbmk4h58PPAwjqnhbgOwmBsIUVrJp3L1fGGq5o"
access_token_secret = "wdPMhCxc8jj3uWkVwDAwlVTCYG6kvFJuWn2bqP08g1OCi"
consumer_key = "DhqgE1tnvTH1KJDNPhkSkzDRZ"
consumer_secret = "Frc9EA7PROJD366dGHj89JZPqqiqlwStK0yAqFoNnbxUsrdn9Y"

twitter_creds = {
    'access_token':access_token,
    'access_token_secret':access_token_secret,
    'consumer_key': consumer_key,
    'consumer_secret':consumer_secret
}

# Logging Formats
MESSAGE_FORMAT_FILE = '%(asctime)s %(levelname)-8s %(name)-12s %(message)s'
MESSAGE_FORMAT_CONSOLE = '%(asctime)s %(levelname)-8s %(message)s'
DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'
FILE_FORMAT = '%Y-%m-%d-%I-%M-%S-%p'


class EngineNode():

    def __init__(self):

        self.init_logger()

        # Acquire Target Location From Server
        url = CONNECT
        res = requests.post(url, data = {'message':'Hello, world!'})

        # Ackowledge connection? TODO handle failed connection
        logging.info(res.json()['message'])

        self.id = res.json()['id']

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
        self.twitter_streamer = TwitterStreamer(twitter_creds,self,southwest, northeast, extras)

    def start(self):
        return self.twitter_streamer.start()

    def stop(self):
        self.twitter_streamer.stop()

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

    try:
        stream_thread = en.start()
    except:
        en.stop()
        stream_thread.join()
        exit()


    #
    # stop the object
    #

    logging.info("Scheduling auto-shutdown")

    t = threading.Timer(30, en.stop)
    t.daemon = True
    t.start()

    t.join()
    stream_thread.join()

    logging.info("All done!")
