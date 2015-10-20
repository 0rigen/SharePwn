import re
import logging

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"


# url_processor #
# This just cleans up a URL by checking for http:// specifier and
# adding it if it doesn't already exit

###################################
#            CheckURL             #
# @url - The url to check and     #
#  verify that http:// is present #
###################################
def checkhttp(url):
    res = re.search("http://", url, re.IGNORECASE)
    if res is None:
        theurl = "http://" + url
        logging.info("Appended HTTP...")
        return theurl
    elif res is not None:
        theurl = url
        logging.info("The URL is already good")
        return theurl

