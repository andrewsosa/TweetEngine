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
CONSUMER_KEY = "DhqgE1tnvTH1KJDNPhkSkzDRZ"
CONSUMER_SECRET = "Frc9EA7PROJD366dGHj89JZPqqiqlwStK0yAqFoNnbxUsrdn9Y"

# Requested Boundaries
SOUTHWEST = (-85,30)
NORTHEAST = (-84,31)

# From central server, edit below
ACCESS_TOKEN = "472058940-Krvbmk4h58PPAwjqnhbgOwmBsIUVrJp3L1fGGq5o"
ACCESS_TOKEN_SECRET = "wdPMhCxc8jj3uWkVwDAwlVTCYG6kvFJuWn2bqP08g1OCi"
NODE_ID = "chilly-rat-80"
