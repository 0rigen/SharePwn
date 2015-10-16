import re

__author__ = '0rigen'

###################################
#            CheckURL             #
# @url - The url to check and     #
#  verify that http:// is present #
###################################
def checkhttp(url):
    res = re.search("http://", url, re.IGNORECASE)
    if res is None:
        theurl = "http://" + url
        return theurl
    elif res is not None:
        theurl = url
        return theurl

