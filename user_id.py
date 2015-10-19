import re
import requests
import url_processor
import logging

__author__ = '0rigen'


# TODO:
# This checks for successful web requests, but will likely need to actually read the page
# and identify if valid data was returned or not.  It may just return a 'successful' but blank
# page if permissions are properly set.

####################################
#      enumerate() users           #
# @start - Integer starting value  #
# @end - Integer ending value      #
####################################
def enumusers(target, start=None, end=None):
    results = []                                                            # Results Container
    failures = []                                                           # Failure Container to retry with Force

    if start is None:                                                       # Assign default Start and End values
        start = 1
        print ("[!] No start value provided, starting at UID=%d" % start)
    if end is None:
        end = 5
        print ("[!] No stop value provided, stopping at UID=%d" % end)

    # Ensure proper target specification
    target = url_processor.checkhttp(target)                                # Check traget formatting

    # Begin requesting pages
    for i in range (start, end):                                            # From start to end...

        r = target + "/UserDisp.aspx?ID=" + str(i)                          # Compiled request string

        try:
            page = requests.get(r)                                          # Open the page
            code_match = re.search("[2**]", str(page.status_code))          # Check for success code 2xx
            if code_match is not None:
                results.append(i)                                           # Add to results if successful
            else:
                failures.append(i)                                          # Add to Failures to retry with Force
        except:                                                             # Handle things that go badly...
            print("[X] Unexpected Error in enumusers()")

    for user in failures:

        r = target + "/UserDisp.aspx?ID=" + str(user) + "?Force=True"        # Request string with True parameter

        try:
            page = requests.get(r)                                          # Open the page
            code_match = re.search("[2**]", str(page.status_code))          # Check for success code 2xx
            if code_match is not None:
                results.append(user)                               # Add to results if successful, remove from Failures
                failures.remove(user)
            else:
                pass
        except:                                                             # Handle things that go badly...
            print("[X] Unexpected Error in enumusers()")

    logging.info("UserID Brute Force Completed.")

    return results                                                          # Return array of successful IDs


# Unit testing....

enumusers("0rigen.net")