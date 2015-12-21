import logging

logging.basicConfig(level=logging.CRITICAL)
# logging.getLogger('suds.client').setLevel(logging.CRITICAL)
# logging.getLogger('suds.transport').setLevel(logging.DEBUG)

from string import ascii_lowercase
from suds.client import Client

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

request_set = ['$', 'SYSTEM', 'AUTHORITY', 'admin', 'Administrator', 'administrator', 'Admin', '\\']


###########################################################
# locate() - Find or specify the location of People.asmx  #
# @target - the url.port couplet of the target            #
# loc - returns the location where People.asmx was found  #
###########################################################
def locate(target):
    # Potential locations
    locations = ['/', '/Search', '/sites/us/en']
    # i = locations.__len__()
    serv = "_vti_bin/People.asmx"

    # Loop over common locations, trying to ID the service
    for option in locations:
        loc = target[0] + option + serv
        # loc = url_processor.checkhttp(loc, target[1]) # This should now be redundant
        r = requests.get(loc)
        if str(r.status_code).startswith("200"):
            print(yellow + "[*] " + endc + "Located People.asmx at: %s" % loc)
            # Now check for the WSDL; this should always be successful
            loc = loc + "?WSDL"
            q = requests.get(loc)
            if str(q.status_code).startswith("200"):
                print(yellow + "[*]" + endc + " Located People WSDL at: %s" % loc)
                return loc  # Returns format: "http://www.site.com/_vti_bin/Service.asmx?WSDL"
            else:
                print(red + "[!]" + endc + "Problem locating the WSDL...this shouldn't have happened")
        else:
            continue

    # If we get this far, we couldn't find People.asmx
    print(yellow + "[!]" + endc + "Failed to locate the People.asmx service in common locations.")
    con = raw_input(yelow + "[?]" + endc + "Specify the location manually? (Y/N): ")
    if con.capitalize() == "Y":
        loc = raw_input(cyan + "[?]" + endc + "URL of People.asmx [Format: http://domain.com/People.asmx]:")
        return loc
    else:
        return None


#############################################
# test_search() does an initial check for   #
# accessibility of the service              #
# @target - the url to try against          #
#############################################
def test_search(target):
    print (yellow + "[*]" + endc + " Performing service test...")
    try:
        req = client.service['PeopleSoap'].SearchPrincipals("a", 5, "All")
        return True
    except:
        return False


###################################################################
# people_search - if the service is accessible, enumerate users
#
# @target - the url of the target sp site
# @text - the string to search for.  ie; "Luke" or "Anakin"
# @results - the number of results to request
# @rtype - the type of data to request, usually All.
###################################################################
def people_search(target, numres, type, specific_string=None, creds=None, cookie=None):
    # Verify input types
    try:

        # Process creds, if any
        if creds is not None:
            print("NTLM Creds not yet supported...ugh >.<")
            # creds = WindowsHttpAuthenticated(username=str(creds[0]), password=str(creds[1]))
            ## Create suds stuff
            # url = target
            # client = Client(url, transport=ntlm)
        elif creds is None:
            url = target
            client = Client(url)

        # Confirm proper input types
        numresults = int(numres)
        restype = str(type)
        search_text = str(specific_string)

    except:
        print(red + "\n[X] " + endc + "Invalid parameter sent to People.asmx searcher" + endc)
        return 1

    # Check to see if the service is accessible...
    if test_search(url) is False:
        print (red + "[!]" + endc + " Error encountered.  You're going to need credentials.")
        return 1

    # If specific_string is not None, do a single search using that string
    if specific_string is not None:
        print (yellow + "[*]" + endc + " Performing search for '%s'" % search_text)
        try:
            req = client.service['PeopleSoap'].SearchPrincipals(search_text, numresults, restype)
            print req
        except:
            print (red + "[!]" + endc + " Error encountered during text search")

    # Otherwise, continue with automatic search...
    # alphabetic search
    else:
        print(green + "\n[*] " + endc + "Beginning alphabetic People search.\n")

        # Perform text enumeration via <searchText> parameter
        try:
            for c in ascii_lowercase:

                print (yellow + "[*]" + endc + " Performing search for '%s'" % str(c))
                try:
                    req = client.service['PeopleSoap'].SearchPrincipals(c, numresults, restype)
                    print req
                    # TODO Cleanly parse through successful alpha results and make the printout look nice
                except:
                    print (red + "[!]" + endc + " Error encountered during character search")
                    break

        except KeyboardInterrupt:
            print(yellow + "[!] " + endc + "Search Interrupted by YOU!\n")
        except:
            print(red + "[!] " + endc + "Unknown error occurred during search\n")

        # Special accounts search
        print(green + "\n[*] " + endc + "Beginning special accounts search.\n")

        # Begin making requests for specialized accounts
        try:
            for s in request_set:

                print (yellow + "[*]" + endc + " Performing search for '%s'" % str(s))
                try:
                    req = client.service['PeopleSoap'].SearchPrincipals(s, numresults, restype)
                    print req
                    # TODO Cleanly parse through successful special results and make the printout look nice
                except:
                    print (red + "[!]" + endc + " Error encountered during special search")
                    break

        except requests.HTTPError:
            logging.error("Got an HTTP error on an already validated People.aspx")

        except:
            print(red + "\n[!] " + endc + "Error returned for searchString %s\n" % s + endc)


# Execution Section
def search(target):
    dst = locate(target)
    if dst is not None:
        people_search(dst, 10, "All")
