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

# Arrays to hold results
successes = []
failures = []


# TODO: Accept cookie authentication
###############################################
#                    geturlsingle             #
# @request - Request response object          #
###############################################
def get_result(request):
    r = request
    status_code = str(r.status_code)

    success_code = re.match("(2)\w", status_code)  # true success, 2xx
    forbid_code = re.match("403", status_code)  # forbidden, but present: 403
    unauth_code = re.match("401", status_code)  # unauthorized, but present: 401
    notfound = re.match("404", status_code)
    # Some SP sites will redirect to error.aspx, catch these
    error_code = re.search('(error\.aspx)', r.url)

    # Unauthorized and Restricted codes are considered successful, as it implies existence
    # First, check if dynamic SharePoint error page was presented
    if error_code is None:
        # Code 2XX
        if success_code is not None:
            successes.append(r.url)
            print(green + "\r[*] Found Open %s <Code %s>" % (r.url, str(r.status_code)) + endc)
        # Code 403
        elif forbid_code is not None:  # Add to the results list if
            successes.append(r.url)  # any kind of success was returned
            print(yellow + "\r[*] Found Restricted %s <Code %s>" % (r.url, str(r.status_code)) + endc)
        # Code 401
        elif unauth_code is not None:
            successes.append(r.url)
            print(yellow + "\r[*] Found Unauthorized %s <Code %s>" % (r.url, str(r.status_code)) + endc)
        # File Not Found error page
        elif notfound is not None:
            failures.append(r.url)
    # Error page was returned (error.aspx)
    elif error_code is not None:
        failures.append(r.url)

    logging.info("[L] Requesting %s => [Returned %s]" % (r.url, str(r.status_code)))
    sys.stdout.flush()

    sys.stdout.flush()  # Remove current request line


###############################################
#                    geturlsingle             #
# @link - a single url                        #
# @urllist - a file containing a list of urls #
# @ntlm - NTLM Auth, user:pass                #
###############################################
def geturl_single(target, link, ntlm=None):
    sys.stdout.flush()
    sys.stdout.write(
            yellow + "\r[...] Requesting: %s%s" % (target[0], link) + endc)  # Write current request to stdout
    page = target[0] + link  # Append page to target domain
    if ntlm is None:
        r = requests.get(page)  # Try to get the page
    elif ntlm is not None:
        r = requests.get(page, HttpNtlmAuth=ntlm)
    get_result(r)


#####################################################
#                    geturllist                     #
# Uses a list of URLs to make a series of requests, #
#   and calls geturlsingle recursively              #
# @target- the target url                           #
# @urllist - a file containing a list of urls       #
# @ntlm - ntlm credentials, user:pass               #
#####################################################
def geturl_list(target, urllist, ntlm=None):
    if urllist is not None:
        try:
            with open(urllist, "r") as infile:  # open the file...
                logging.info("file %s" % infile + " opened.")
                for line in infile:
                    line = line.rstrip()  # Clean up the input line
                    if ntlm is None:
                        geturl_single(target, line)  # Call self on that url individually
                    if ntlm is not None:
                        geturl_single(target, line, ntlm)
        except:
            print(red + "[!]" + endc + " Problem accessing urllist.  Check permissions.")
    return successes
