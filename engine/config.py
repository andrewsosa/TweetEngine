import os

#
#   Tweet Engine node configuration.
#

VERSION     = 1.0

# Server URLS
BASE_ADDR   = "http://localhost:8080/engine"   # Address of primary server.
REGISTER    = BASE_ADDR + "/register"
CONNECT     = BASE_ADDR + "/connect"
POST        = BASE_ADDR + "/upload"
status      = BASE_ADDR + "/status"

# Logging Formats
MESSAGE_FORMAT_FILE = '%(asctime)s %(levelname)-8s %(name)-12s %(message)s'
MESSAGE_FORMAT_CONSOLE = '%(asctime)s %(levelname)-8s %(message)s'
DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'
FILE_FORMAT = '%Y-%m-%d-%I-%M-%S-%p'

# Twitter API Credentials
CONSUMER_KEY = os.environ['TWEET_ENGINE_CONSUMER_KEY']          # Only for
CONSUMER_SECRET = os.environ['TWEET_ENGINE_CONSUMER_SECRET']    # private server

# Requested Boundaries
SOUTHWEST = (-85,30)
NORTHEAST = (-81,34)

# From central server, edit below
ACCESS_TOKEN = "<access_token>"
ACCESS_TOKEN_SECRET = "<access_token_secret>"
NODE_ID = "<node_id>"
