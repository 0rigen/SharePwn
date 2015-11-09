import logging
import re

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"


# url_processor #
# This just cleans up a URL by checking for http:// specifier and
# adding it if it doesn't already exit

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
            theurl = url[0]
            logging.info("The URL is already good")
            return theurl
    if port == 443:
        res = re.search("https://", url, re.IGNORECASE)
        if res is None:
            theurl = "https://" + url
            logging.info("Appended HTTPS...")
            return theurl
    else:
        print ("[!] Non-standard ports not yet supported!")
        # TODO: Handle non-standard port specifications
