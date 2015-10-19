import re
import requests
import url_processor
import url_requester

__author__ = '0rigen'


####################################
#      enumerate() users           #
# @start - Integer starting value  #
# @end - Integer ending value      #
####################################
def enumusers(target, start=None, end=None):
    # Default Start and End values
    if start is None:
        start = 1
        print ("[!] No start value provided, starting at UID=%d" % start)
    if end is None:
        end = 5
        print ("[!] No stop value provided, stopping at UID=%d" % end)

    # Ensure proper target specification
    target = url_processor.checkhttp(target)

    # Begin requesting pages
    for i in range (start, end):
        # Create request URL
        r = target + "/UserDisp.aspx?ID=" + str(i)
        # Call geturlcode()
        try:
            url_requester.geturlcode(r,None)
        except:
            print("[X] Unexpected Error in enumusers()")


# Unit testing....

enumusers("0rigen.net")