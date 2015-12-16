import logging
import sys
from string import ascii_lowercase
# TODO Use BeautifulSoup to parse the XML responses from asmx service
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

# TODO Try and spoof request as if it were coming from the local machine
# host resolution, then spoof in packet?

people_headers = """POST /_vti_bin/People.asmx HTTP/{{http}}
Host: {{Target}}
Content-Type: text/xml; charset=utf-8
Content-Length: {{length}}
SOAPAction: "http://schemas.microsoft.com/sharepoint/soap/SearchPrincipals"
"""
people_data = """<?xml version="1.0" encoding="utf-8"?>
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


######################################################################
# create_header creates a custom header for each unique request      #
# @target -  the target domain like sp.domain.com                    #
# @location - the People.asmx location, like /_vti_bin/People.asmx   #
# @ http - the HTTP version to use; defaults to 1.1 if not provided  #
# ret_header - the custom header to be returned                      #
######################################################################
def create_header(target, location, agent=None, http=None):
    # Default to HTTP/1.1
    if http is None:
        http = "1.1"
    # Fill in the blanks...
    # ret_header = people_headers.replace("{{location}}", location)
    ret_header = people_headers.replace("{{Target}}", target[0])
    ret_header = ret_header.replace("{{http}}", http)
    ret_header = ret_header.replace("{{length}}", "1")
    return ret_header


###########################################################
# locate() - Find or specify the location of People.asmx  #
# @target - the url.port couplet of the target            #
# loc - returns the location where People.asmx was found  #
###########################################################
# TODO Need to change how I do this.  The /_vti_bin/People.asmx is constant
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
            return loc
        # i+=1
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


###########################################################
# find_service - determine if People.asmx is accessible
# @target - the target site
# destination - returns full url of the found service
###########################################################
def find_service(target):
    url = target[0]
    fakeagent = "'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'"
    # port = target[1] # Unused

    destination = locate(target)

    # Set XML Values for dummy request
    # TODO Move this into a create_payload() function
    header = create_header(target, destination, fakeagent, "1.1")
    payload = people_data.replace("{{searchString}}", "a")
    payload = payload.replace("{{maxResults}}", "100")
    payload = payload.replace("{{principalType}}", "All")

    logging.info("\nBuilding People.asmx dummy POST Request\n")

    # Build dummy Packet and test responsiveness
    # payload = data

    sys.stdout.write(yellow + "\n[*] " + endc + "Sending test request to %s\n" % destination + endc)
    try:
        # TODO Move this stuff into a test connection type of method
        # I have to manually specify the content-type, or requests will use the wrong format and the request returns 415 code
        req = requests.post(destination, data=payload, allow_redirects=True,
                            headers={"Content-Type": "text/xml; charset=utf-8"})

        logging.info("Dummy request sent to People.aspx")

        # Request seemed to work
        if str(req.status_code).startswith("2"):
            print(
                green + "\n[*] " + endc + "Received Status %s.  People search is available and not locked down!\n" % str(
                        req.status_code) + endc)
            logging.info("Received a 2XX Status for People.aspx")
            return destination

        # Service is locked down
        elif str(req.status_code).startswith("403") or str(req.status_code).startswith("401"):
            print(
                yellow + "\n[!] " + endc + "Received Status %s.  You do not have permission to use the service. \n" % req.status_code + endc)
            return None

        # Bad Request - something weird happened...
        elif str(req.status_code).startswith("400"):
            print(red + "[!]" + endc + " Received HTTP 400 Response: Bad Request.  hmmm...")

        # All else
        else:
            print(yellow + "\n[!] " + endc + "Received Unexpected Status %s" % str(req.status_code) + endc)
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
    try:
        for c in ascii_lowercase:

            # Build the request body
            data = people_data.replace("{{maxResults}}", str(numresults))  # Set max results value
            data = data.replace("{{principalType}}", restype)  # Set principalType value
            data = data.replace("{{searchString}}", c)  # Set searchString to single character
            payload = data

            try:
                r11 = requests.post(target, data=payload)  # Send a request with new searchString
                logging.info("Request sent to People.aspx with searchString %s" % c)

                ## *** PARSE RESULTS *** ## INCOMPLETE
                print(green + "\n[*] " + endc + "This is where the results go for %s\n" % c + endc)
                soup = BS(r11.content)
                print soup.find('AccountName').text

            except requests.HTTPError:
                logging.error(
                        red + "[!] " + endc + "Got an HTTP error on an already validated People.aspx..That's bad!" + endc)
            except:
                print(red + "\n[!] " + endc + "Error returned for searchString %s\n" % c + endc)

    except KeyboardInterrupt:
        print(yellow + "[!] " + endc + "Search Interrupted by YOU!\n")
    except:
        print(red + "[!] " + endc + "Unknown error occurred during search\n")

    # Special accounts search
    print(green + "\n[*] " + endc + "Beginning special accounts search.\n")

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
