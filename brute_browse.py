import logging
import re
import sys

import requests

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"

successes = []
failures = []


###############################################
#                    geturlcode               #
# @link - a single url                        #
# @urllist - a file containing a list of urls #
###############################################
def geturlcode(target, link=None, urllist=None):
    ############################################################
    # If 'link' is none, then we should have a list.           #
    # A list is processed with recursive calls to geturlcode() #
    # with a single link (line) argument read from the file.   #
    # Link and file can be passed in simultaneously, and will  #
    # handle the singe link followed by the list               #
    ############################################################
    # If a single URL is given
    if link is not None:
        sys.stdout.flush()
        sys.stdout.write("\r[...] Requesting: %s%s" % (target, link))  # Write current request to stdout
        page = target + link  # Append page to target domain
        page.replace("\n", "")  # Remove stray newlines

        r = None
        try:
            r = requests.get(page)                                      # Try to get the page
        except:
            pass                                                        # Ignore HTTP errors and keep going

        if r is not None:
            status_code = str(r.status_code)

            success_code = re.match("(2)\w", status_code)                        # true success, 2xx
            forbid_code = re.match("403", status_code)                           # forbidden, but present: 403
            unauth_code = re.match("401", status_code)                           # unauthorized, but present: 401
            notfound = re.match("404", status_code)

            if success_code is not None:
                successes.append(page)
                print("\r[*] Found Open %s <Code %s>" % (page, str(r.status_code)))
            elif forbid_code is not None:  # Add to the results list if
                successes.append(page)  # any kind of success was returned
                print("\r[*] Found Restricted %s <Code %s>" % (page, str(r.status_code)))
            elif unauth_code is not None:
                successes.append(page)
                print("\r[*] Found Unauthorized %s <Code %s>" % (page, str(r.status_code)))
            elif notfound is not None:
                failures.append(page)

            logging.info("[L] Requesting %s => [Returned " % l + str(r.status_code) + "]")
            sys.stdout.flush()

        else:
            pass  # Just keep going if 4xx or 5xx error encountered

        sys.stdout.flush()  # Remove current request line

    # If a file list of URLs is given
    if urllist is not None:
        with open(urllist, "r") as infile:                                      # open the file...
            logging.info("file %s" % infile + " opened.")
            for line in infile:
                line = line.rstrip()                                            # Clean up the input line
                geturlcode(target, line, None)                                  # Call self on that url individually

    # If neither were passed in... this function was called incorrectly
    else:
        print("Something went wrong!  Quitting...")
        logging.error("geturlcode() did not receive any valid parameters")
        sys.exit(1)

    # Finished processing individual item or List, return array of successful requests...
    return successes


def auto_browse():
    with open("service_list.txt", "r") as srvlist:
        for line in srvlist:
            geturlcode("0rigen.net", line, None)
