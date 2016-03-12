import re, requests

from config import REGISTER

# This pattern matches node IDs.
PATTERN = r"[a-z]+-[a-z]+-[0-9]{1,3}"
regex = re.compile(PATTERN)

if __name__ == "__main__":

    # Grab out new ID from the server.
    url = REGISTER
    res = requests.get(url)
    nodeID = res.json()['id']
    print "Assigned identifier " + nodeID

    # Let's try and write it to the file.
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
