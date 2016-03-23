import re, requests, webbrowser

from config import REGISTER

if __name__ == "__main__":

    # Grab out new ID from the server.
    try:
        url = REGISTER
        webbrowser.open(url, autoraise=True)
    except:
        print "No default web browser available."
