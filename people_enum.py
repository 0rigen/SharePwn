import logging
import sys
from string import ascii_lowercase

import requests
import url_processor

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"

red = "\033[31m"  # usually for errors, [X] items
cyan = "\033[36m"
yellow = "\033[33m"  # usually for information and requests, the [?] items
green = "\033[92m"  # Information and success, [!]
blue = "\033[94m"
endc = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"

people_headers = """
POST /_vti_bin/People.asmx HTTP/1.0
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


# TODO Determine if People.asmx exists in root web directory or under a common subfolder like Search
# TODO Determine if requests is using the correct HTTP version without my interaction; wireshark it?

############################################################################################
# Uses the people.asmx service to enumerate users, systems, and other accounts.  Begins by
# performing a response test to see if  the service is properly locked down; abandons
# the call if an access error is received.
#
# @target - the url of the target sp site
# @text - the string to search for.  ie; "Luke" or "Anakin"
# @results - the number of results to request
# @rtype - the type of data to request, usually All.
############################################################################################

def people_enum(target, text, results, rtype):
    gogogo = False

    url = target[0]
    port = target[1]

    # Verify input types
    try:
        numresults = int(results)
        restext = str(text)
        restype = str(rtype)
    except:
        print(red + "[X] Invalid parameter sent to People.asmx searcher" + endc)
        return 1

    t = url_processor.checkhttp(url, port)
    destination = t + "/Search/_vti_bin/People.asmx"

    # Set XML Values for dummy request
    head = people_headers.replace("{{Target}}", url)
    data = people_data.replace("{{searchString}}", restext)
    data = data.replace("{{maxResults}}", str(numresults))
    data = data.replace("{{principalType}}", restype)

    logging.info("\nBuilding People.asmx dummy POST Request with the following parameters: \n")
    logging.info("%s, %s, %s, %s" % (url, restext, str(numresults), restype))

    # Build dummy Packet and test responsiveness
    payload = data

    #
    # This does not yet send requests to non-standard ports... TODO Enumerate users on non-standard ports
    #

    sys.stdout.write(yellow + "\n[*] Sending test request to %s\n" % (destination) + endc)
    try:

        # Send a dummy request to see if it gets processed
        r = requests.post(destination, data=payload)
        logging.info("Dummy request sent to People.aspx")

        if str(r.status_code).startswith("2"):
            print(green + "\n[*] Received Status %s.  People search is available.\n" % str(r.status_code) + endc)
            logging.info("Received a 2XX Status for People.aspx")
            gogogo = True

        else:
            print(yellow + "\n[!] Received Unexpected Status %s" % str(r.status_code) + endc)

    except requests.HTTPError:
        print(red + "\n[X] Error Received.  People.asmx Service is locked down or not there.\n" + endc)
    except:
        print(red + "\n[!] Unknown error during People enumeration\n" + endc)

    if gogogo == True:

        print(green + "\n[*] Beginning alphabetic People search.\n")

        # Perform text enumeration via <searchText> parameter
        for c in ascii_lowercase:

            # Build the request body
            data = people_data.replace("{{maxResults}}", str(numresults))       # Set max results value
            data = data.replace("{{principalType}}", restype)                   # Set principalType value
            data = data.replace("{{searchString}}", c)                          # Set searchString to single character
            payload = data

            try:
                r = requests.post(destination, data=payload)                # Send a request with new searchString
                logging.info("Request sent to People.aspx with searchString %s" % c)

                # TODO: Regex to filter through returned results and print them here
                print(green + "\n[*] This is where the results go for %s\n" % c + endc)
                #
                #
                # regex to match <AccountName> and </AccountName>
                # (?:</?AccountName>)
                # <AccountName>.*</?AccountName>

            except requests.HTTPError:
                logging.error(red + "[!] Got an HTTP error on an already validated People.aspx" + endc)

            except:
                print(red + "\n[!] Error returned for searchString %s\n" % c + endc)

        print("\n[*] Beginning special accounts search.\n")

        # Begin making requests for specialized accounts
        for s in request_set:

            # Build the request body
            data = people_data.replace("{{maxResults}}", str(numresults))       # Set max results value
            data = data.replace("{{principalType}}", restype)                   # Set principalType value
            data = data.replace("{{searchString}}", c)                      # Set searchString to single character
            payload = data

            try:
                r = requests.post(destination, data=payload)                # Send a request with new searchString
                logging.info("Request sent to People.aspx with searchString %s" % s)

                # TODO: Regex to filter through returned results and print them here
                print(green + "[*] This is where the results go for %s" % s + endc)
                #
                #

            except requests.HTTPError:
                logging.error("Got an HTTP error on an already validated People.aspx")

            except:
                print(red + "\n[!] Error returned for searchString %s\n" % s + endc)

    elif gogogo == False:
        print(red + "\n[!] People service is locked down or non-existent.\n" + endc)
