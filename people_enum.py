import httplib
import logging
import sys
from string import ascii_lowercase

import requests
import url_processor

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

# Although this header is declared, requests does not use it currently.  If I need this,
# I'll have to manually tell it to use this header data.
people_headers = """
POST /_vti_bin/People.asmx HTTP/{{http}}
Host: {{Target}}
Content-Type: text/xml; charset=utf-8
Content-Length: {{length}}
SOAPAction: "http://schemas.microsoft.com/sharepoint/soap/SearchPrincipals"
"""
people_data = """
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <SearchPrincipals xmlns="http://schemas.microsoft.com/sharepoint/soap/">
            <searchText>{{searchString}}</searchText>
            <maxResults>{{maxResults}}</maxResults>
            <principalType>{{principalType}}</principalType>
        </SearchPrincipals>
   </soap:Body>
</soap:Envelope>
"""

request_set = ['$', 'SYSTEM', 'AUTHORITY', 'admin', 'Administrator', 'administrator', 'Admin', '\\']


###########################################################
# locate() - Find or specify the location of People.asmx  #
# @target - the url.port couplet of the target            #
# loc - returns the location where People.asmx was found  #
###########################################################
def locate(target):
    # Potential locations
    locations = ['/', '/Search']
    serv = "_vti_bin/People.asmx"
    for option in locations:
        loc = target[0] + option + serv
        loc = url_processor.checkhttp(loc, target[1])
        r = requests.get(loc)
        if str(r.status_code).startswith("200"):
            print(yellow + "[*] " + endc + "Located People.asmx at: %s" % loc)
            return loc


###########################################################
# find_service - determine if People.asmx is accessible
# @target - the target site
# destination - returns full url of the found service
###########################################################
def find_service(target):
    url = target[0]
    # port = target[1] # Unused

    destination = locate(target)

    # Set XML Values for dummy request
    # head = people_headers.replace("{{Target}}", url) # Unused
    data = people_data.replace("{{searchString}}", "a")
    data = data.replace("{{maxResults}}", "100")
    data = data.replace("{{principalType}}", "All")

    logging.info("\nBuilding People.asmx dummy POST Request\n")

    # Build dummy Packet and test responsiveness
    payload = data

    sys.stdout.write(yellow + "\n[*] " + endc + "Sending test request to %s\n" % destination + endc)
    try:
        # Manually force HTTP/1.1
        httplib.HTTPConnection._http_vsn = 10
        httplib.HTTPConnection._http_vsn_str = 'HTTP/1.1'
        # Send a dummy request to see if it gets processed
        r11 = requests.post(destination, data=payload)
        logging.info("Dummy request sent to People.aspx via HTTP/1.1")

        if str(r11.status_code).startswith("2"):
            print(
            green + "\n[*] " + endc + "Received Status %s.  People search is available and not locked down!\n" % str(
                r11.status_code) + endc)
            logging.info("Received a 2XX Status for People.aspx")
            return destination
        elif str(r11.status_code).startswith("40"):
            print(
                yellow + "\n[!] " + endc + "Received Status %s.  People search is properly locked down! :) \n" % r11.status_code + endc)
            return None
        else:
            print(yellow + "\n[!] " + endc + "Received Unexpected Status %s" % str(r11.status_code) + endc)
            return None

    except requests.HTTPError:
        print(red + "\n[X] " + endc + "Error Received.  People.asmx Service is locked down or not there.\n" + endc)
    except:
        print(red + "\n[!] " + endc + "Unknown error during People enumeration\n" + endc)


###################################################################
# people_search - if the service is accessible, enumerate users
#
# @target - the url of the target sp site
# @text - the string to search for.  ie; "Luke" or "Anakin"
# @results - the number of results to request
# @rtype - the type of data to request, usually All.
###################################################################
def people_search(target, numres, type):
    # Verify input types
    try:
        numresults = int(numres)
        restype = str(type)
    except:
        print(red + "[X] " + endc + "Invalid parameter sent to People.asmx searcher" + endc)
        return 1

    # alphabetic search
    print(green + "\n[*] " + endc + "Beginning alphabetic People search.\n")

    # Perform text enumeration via <searchText> parameter
    for c in ascii_lowercase:

        # Build the request body
        data = people_data.replace("{{maxResults}}", str(numresults))  # Set max results value
        data = data.replace("{{principalType}}", restype)  # Set principalType value
        data = data.replace("{{searchString}}", c)  # Set searchString to single character
        payload = data

        try:
            r11 = requests.post(destination, data=payload)  # Send a request with new searchString
            logging.info("Request sent to People.aspx with searchString %s" % c)

            # TODO: Regex to filter through returned results and print them here
            print(green + "\n[*] " + endc + "This is where the results go for %s\n" % c + endc)
            # regex to match <AccountName> and </AccountName>
            # (?:</?AccountName>)
            # <AccountName>.*</?AccountName>

        except requests.HTTPError:
            logging.error(
                red + "[!] " + endc + "Got an HTTP error on an already validated People.aspx..That's bad!" + endc)

        except:
            print(red + "\n[!] " + endc + "Error returned for searchString %s\n" % c + endc)

    # Special accounts search
    print("\n[*] " + endc + "Beginning special accounts search.\n")

    # Begin making requests for specialized accounts
    for s in request_set:

        # Build the request body
        data = people_data.replace("{{maxResults}}", str(numresults))  # Set max results value
        data = data.replace("{{principalType}}", restype)  # Set principalType value
        data = data.replace("{{searchString}}", s)  # Set searchString to single character
        payload = data

        try:
            r11 = requests.post(destination, data=payload)  # Send a request with new searchString
            logging.info("Request sent to People.aspx with searchString %s" % s)

            # TODO: Regex to filter through returned results and print them here
            print(green + "[*] " + endc + "This is where the results go for %s" % s + endc)

        except requests.HTTPError:
            logging.error("Got an HTTP error on an already validated People.aspx")

        except:
            print(red + "\n[!] " + endc + "Error returned for searchString %s\n" % s + endc)


# Execution Section
def search(target):
    dst = find_service(target)
    if dst is not None:
        people_search(dst, 1000, "All")
