import logging
import re

import requests
import url_processor

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"


# SP Versions are identified in the response headers as 'MicrosoftSharePointTeamServices': 'X.X.X.X'
# Identify SP versions via initial GET request
# 2010 will start with 14, like 14.0.0.6010
# 2013 will start with 15.
# 2007 will start with 12.
# 2003 will start with 6.

# TODO This module is not yet called by the main program - need to add it and determine what difference
# TODO  it makes to the primary interrogation functions.

####################################################
# identify                                         #
# Record a response from the target and examines   #
# the headers for SP version information           #
# @url - the target                                #
# @ port - the target port                         #
####################################################
def identify(url, port=None):
    # TODO: Use the servreg and aspreg to also identify server software and asp version information, if present

    # Regex to look for #.#.#.# format, where # is 1 or more numbers, dot separated
    spreg = re.compile("[\']([6,12,14,15]+\.)+(\d+\.)+(\d+\.)+(\d*)[\']")
    # Regex to identify Server in use
    # TODO servreg = re.compile("[\']Server[\']: [\'].*[\']")
    # Regex to idnetify ASP version, if any
    # TODO aspreg = re.compile("[\']X-AspNet-Version[\']: [\'](\d+\.)?(\d+\.)?(\d+\.)?(\d*)[\']")

    # Process the link, if port is specified
    if port is not None:
        link = url_processor.checkhttp(url, port)
    else:
        link = url

    # Request the page
    r = requests.get(link)

    # Check for a successful response
    status_code = str(r.status_code)
    success_code = re.match("(2)\w", status_code)  # Check for successful response code

    if success_code is None:  # Return 'Unknown' if request unsuccessful
        print("[!] Unsuccessful request when attempting to identify SP version.  Version remains Unknown...")
        logging.info("Version ID failed; did not sp_match 2xx response regex")
        return "Unknown"

    # Search for version info in headers
    sp_match = re.search(spreg, str(r.headers))  # Otherwise, keep working
    # TODO asp_match = re.search(aspreg, str(r.headers))
    # TODO serv_match = re.search(servreg, str(r.headers))

    if sp_match is None:  # No version info returned
        print("[!] No SharePoint version information returned.")
        logging.info("Version ID failed; successful request but no version information found.")
        return "Unknown"
    else:
        ver = str(sp_match.group())  # Store the version info and return
        print("[*] SharePoint version identified as %s" % ver)
        logging.info("Version ID successful. Found %s" % ver)
        return ver
