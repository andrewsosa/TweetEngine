import re, requests, webbrowser

from config import REGISTER

# This pattern matches node IDs.
PATTERN = r"[a-z]+-[a-z]+-[0-9]{1,3}"
regex = re.compile(PATTERN)

# Write the nodeID to the config file
def export_id(nodeID):
    try:

        f = open('config.py','r')
        filedata = f.read()
        f.close()

        newdata = regex.sub(nodeID, filedata)
        newdata = newdata.replace("<nodeID>", nodeID)

        f = open('config.py','w')
        f.write(newdata)
        f.close()

    except:
        print "Unable to automatically update config.py, please add ID manually."

if __name__ == "__main__":

    # Grab out new ID from the server.
    try:
        url = REGISTER
        webbrowser.open(url, autoraise=True)
    except:
        print "No default web browser available."
