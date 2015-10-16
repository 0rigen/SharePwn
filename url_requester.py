import requests
import url_processor
import sys
import logging

__author__ = '0rigen'


###############################################
#                    geturlcode               #
# @link - a single url                        #
# @urllist - a file containing a list of urls #
###############################################
def geturlcode(link=None, urllist=None):

    # If a single URL is given
    if link is not None:
        l = url_processor.checkhttp(link)                                      # Check/add HTTP protocol
        r = requests.get(l)                                                    # Get the page
        print("%s" % l + " returned Code %s " % str(r.status_code))            # Print the result
        logging.info("* Requesting %s => [Returned " % l + str(r.status_code)+"]")

    # If a file list of URLs is given
    elif urllist is not None:
        with open(urllist, "r") as infile:                                      # open the file...
            logging.info("file %s" % infile + " opened.")
            for line in infile:
                line = url_processor.checkhttp(line)                            # Check/add HTTP protocol
                line = line.rstrip()                                            # Clean up the input line
                geturlcode(line,)                                               # Call self on that url individually
    else:
        print("Something went wrong!  Quitting...")
        logging.error("geturlcode() did not receive any valid parameters")
        sys.exit(1)


#print("Welcome to test land...\n")
#logging.basicConfig(stream=sys.stdout, level=logging.INFO)
#geturlcode(None,"test_urllist.txt")