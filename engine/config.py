#
#   Tweet Engine node configuration.
#

# Server URLS
BASE_ADDR   = "http://localhost:8080/engine"   # Address of primary server.
REGISTER    = BASE_ADDR + "/register"
CONNECT     = BASE_ADDR + "/connect"
POST        = BASE_ADDR + "/upload"


# Logging Formats
MESSAGE_FORMAT_FILE = '%(asctime)s %(levelname)-8s %(name)-12s %(message)s'
MESSAGE_FORMAT_CONSOLE = '%(asctime)s %(levelname)-8s %(message)s'
DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'
FILE_FORMAT = '%Y-%m-%d-%I-%M-%S-%p'

# Twitter API Credentials
access_token = "***REMOVED***"
access_token_secret = "***REMOVED***"
consumer_key = "***REMOVED***"
consumer_secret = "***REMOVED***"

twitter_creds = {
    'access_token':access_token,
    'access_token_secret':access_token_secret,
    'consumer_key': consumer_key,
    'consumer_secret':consumer_secret
}

# Node ID
NODE_ID = "funny-parrot-94"
