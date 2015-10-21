import url_processor
import sys
import requests
import logging
from string import ascii_lowercase

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"

people_headers = """
POST /_vti_bin/People.asmx HTTP/1.0
Host: {{Target}}
Content-Type: text/xml; charset=utf-8
Content-Length: {{length}}
SOAPAction: "http://schemas.microsoft.com/sharepoint/soap/SearchPrincipals"
"""
people_data = """
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelop/">
    <soap:Body>
        <SearchPrincipals xmlns="http://schemas.microsoft.com/sharepoint/soap/">
            <searchText>{{searchString}}</searchText>
            <maxResults>{{maxResults}}</maxResults>
            <principalType>{{principalType}}</prinicpalType>
        </SearchPrincipals>
   </soap:Body>
</soap:Envelope>
"""

request_set = ['$', 'SYSTEM', 'AUTHORITY', 'admin', 'Administrator', 'administrator', 'Admin', '\\']


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

    # Chop off HTTP if it is present
    target = target.replace("http://", "")
    target = target.replace("HTTP://", "")

    # Verify input types
    try:
        numresults = int(results)
        restext = str(text)
        restype = str(rtype)
    except:
        print("Invalid parameter sent to People.asmx searcher")
        return 1

    t = url_processor.checkhttp(target)
    destination = t + "/_vti_bin/People.asmx"

    # Set XML Values for dummy request
    head = people_headers.replace("{{Target}}", target)
    data = people_data.replace("{{searchString}}", restext)
    data = data.replace("{{maxResults}}", str(numresults))
    data = data.replace("{{principalType}}", restype)

    logging.info("\nBuilding People.asmx dummy POST Request with the following parameters: \n")
    logging.info("%s, %s, %s, %s" % (target, restext, str(numresults), restype))

    # Build dummy Packet and test responsiveness
    payload = data
    sys.stdout.write("\n[*] Sending test request to %s\n" % destination)
    try:

        # Send a dummy request to see if it gets processed
        r = requests.post(destination, data=payload)
        logging.info("Dummy request sent to People.aspx")

        # Check status_code for error or success
        if re.match("4..", r.status_code) is not None:
            print("\n[!] Received Status %s.  Cannot continue.\n" % str(r.status_code))
            logging.info("Got a 4XX error for People.aspx")
            gogogo= False

        elif re.match("2..", r.status_code) is not None:
            print("\n[*] Received Status %s.  People search is available.\n" % str(r.status_code))
            logging.info("Received a 2XX Status for People.aspx")
            gogogo = True

    except requests.HTTPError:
        print("\n[!] Error Received.  People.asmx Service is locked down or not there.\n")
    except:
        print("\n[!] Unknown error during People enumeration\n")

    if gogogo == True:
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
                print("\n[*] This is where the results go for %s\n" % c)
                #
                #
                # regex to match <AccountName> and </AccountName>
                # (?:</?AccountName>)
                # <AccountName>.*</?AccountName>


            except requests.HTTPError:
                logging.error("Got an HTTP error on an already validated People.aspx")

            except:
                print("\n[!] Error returned for searchString %s\n" % c)

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
                print("[*] This is where the results go for %s" % s)
                #
                #

            except requests.HTTPError:
                logging.error("Got an HTTP error on an already validated People.aspx")

            except:
                print("\n[!] Error returned for searchString %s\n" % s)

    elif gogogo == False:
        print("\n People service is locked down.\n")

# Unit Tests...
people_enum("http://0rigen.net", "text", 20, "All")