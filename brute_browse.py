import logging
import re
import sys

import requests

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Development"

red = "\033[31m"  # usually for errors, [X] items
cyan = "\033[36m"
yellow = "\033[33m"  # usually for information and requests, the [?] items
green = "\033[92m"  # Information and success, [!]
blue = "\033[94m"
endc = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"

successes = []
failures = []


###############################################
#                    geturlcode               #
# @link - a single url                        #
# @urllist - a file containing a list of urls #
###############################################
def geturl_single(target, link):
    if link is not None:
        sys.stdout.flush()
        sys.stdout.write(
                yellow + "\r[...] Requesting: %s%s" % (target[0], link) + endc)  # Write current request to stdout
        page = target[0] + link  # Append page to target domain

        r = requests.get(page)  # Try to get the page

        status_code = str(r.status_code)

        success_code = re.match("(2)\w", status_code)  # true success, 2xx
        forbid_code = re.match("403", status_code)  # forbidden, but present: 403
        unauth_code = re.match("401", status_code)  # unauthorized, but present: 401
        notfound = re.match("404", status_code)

        # Unauthorized and Restricted codes are considered successful, since it indicates their
        # existence indirectly.
        if success_code is not None:
            successes.append(page)
            print(green + "\r[*] Found Open %s <Code %s>" % (page, str(r.status_code)) + endc)
        elif forbid_code is not None:  # Add to the results list if
            successes.append(page)  # any kind of success was returned
            print(yellow + "\r[*] Found Restricted %s <Code %s>" % (page, str(r.status_code)) + endc)
        elif unauth_code is not None:
            successes.append(page)
            print(yellow + "\r[*] Found Unauthorized %s <Code %s>" % (page, str(r.status_code)) + endc)
        elif notfound is not None:
            failures.append(page)

        logging.info("[L] Requesting %s => [Returned %s]" % (page, str(r.status_code)))
        sys.stdout.flush()

        sys.stdout.flush()  # Remove current request line

    else:
        print(red + "[X] geturl_single did not receive a valid argument!" + endc)
        logging.error("geturl_list() did not receive any valid parameters")


def geturl_list(target, urllist):
    if urllist is not None:
        with open(urllist, "r") as infile:  # open the file...
            logging.info("file %s" % infile + " opened.")
            for line in infile:
                line = line.rstrip()  # Clean up the input line
                geturl_single(target, line)  # Call self on that url individually

    # Incorrect function call
    else:
        print(red + "[X] geturl_list did not receive a valid argument!" + endc)
        logging.error("geturl_list() did not receive any valid parameters")
        sys.exit(1)

    return successes
