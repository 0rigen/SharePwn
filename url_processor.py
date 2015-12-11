import logging
import re

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"


# url_processor #
# This just cleans up a URL by checking for http:// specifier and
# adding it if it doesn't already exit

red = "\033[00;31m"  # usually for errors, [X] items
cyan = "\033[00;36m"
yellow = "\033[00;33m"  # usually for information and requests, the [?] items
green = "\033[00;32m"  # Information and success, [!]
blue = "\033[00;34m"
endc = '\033[0m'
bold = '\033[1m'
underline = '\033[4m'

################################################
#            CheckURL                          #
# @url - The url to check                      #
# @port - the port number, to specify protocol #
################################################
def checkhttp(url, port):
    if port == 80:
        res = re.search("http://", url, re.IGNORECASE)
        if res is None:
            theurl = "http://" + url
            logging.info("Appended HTTP...")
            return theurl
        elif res is not None:
            theurl = url
            logging.info("The HTTP link is already good")
            return theurl
    if port == 443:
        res = re.search("https://", url, re.IGNORECASE)
        if res is None:
            theurl = "https://" + url
            logging.info("Appended HTTPS...")
            return theurl
        elif res is not None:
            theurl = url
            logging.info("The HTTPS link is already good")
            return theurl
    else:
        print (cyan + "[!] Non-standard ports not yet supported!" + endc)
        # TODO: Handle non-standard port specifications
