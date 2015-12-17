import logging
import re

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Development"

# url_processor #
# This just cleans up a URL by checking for http:// specifier and
# adding it if it doesn't already exit

red = "\033[31m"  # usually for errors, [X] items
cyan = "\033[36m"
yellow = "\033[33m"  # usually for information and requests, the [?] items
green = "\033[92m"  # Information and success, [!]
blue = "\033[94m"
endc = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"


################################################
#            CheckURL                          #
# @url - The url to check                      #
# @port - the port number, to specify protocol #
################################################
def checkhttp(url, port):
    if port == 80:
        http = re.compile("http://", re.IGNORECASE)
        https = re.compile("https://", re.IGNORECASE)
        httpres = http.match(url)
        httpsres = https.match(url)

        if httpres is None and httpsres is None:  # No HTTP specification of either kind
            theurl = "http://" + url
            logging.info("Appended HTTP...")
            return theurl
        elif httpsres is not None:  # HTTPS found, fix it
            print(cyan + "[!]" + endc + " Found a port/protocol mismatch.  Fixing it for you! :D  ...")
            logging.info("The HTTP link was prepended by HTTPS, fixing it.")
            theurl = https.sub("http://", url)
            return theurl
        elif httpres is not None:  # HTTP found
            theurl = url
            logging.info("The HTTP link is already good")
            return theurl
    if port == 443:
        https = re.compile("https://", re.IGNORECASE)
        http = re.compile("http://", re.IGNORECASE)
        httpres = http.match(url)
        httpsres = https.match(url)

        if httpres is None and httpsres is None:  # No HTTP specification of either kind
            theurl = "https://" + url
            logging.info("Appended HTTPS...")
            return theurl
        elif httpres is not None:  # HTTP found, fix it
            print(cyan + "[!]" + endc + " Found a port/protocol mismatch.  Fixing it for you! :D  ...")
            logging.info("The HTTPS link was prepended by HTTP, fixing it.")
            theurl = http.sub("https://", url)
            return theurl
        elif httpsres is not None:
            theurl = url
            logging.info("The HTTPS link is already good")
            return theurl
    else:
        print (cyan + "[!] Non-standard ports not yet supported!" + endc)
        return None  # Indicate that a bad port was used
        # TODO: Handle non-standard port specifications
