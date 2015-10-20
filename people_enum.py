from scapy.all import sr1, IP
import url_processor
import sys

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


###############################################
# Uses the people.asmx service to enumerate
# users, systems, and other accounts.
##############################################

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
    sys.stdout.write("[*] Sending requests to %s\n" % destination)

    # Loop through the alphabet, A-Z, using RegEx to locate the different fields that will be returned by
    # an All request... to include User Name, UserID, OU, Email, etc.
    # Then, perform non-alphabetic or keyword searches
    # - $
    # - SYSTEM
    # - DC
    # - _
    # - admin
    # - administrator
    # These can reveal great information about system and admin accounts

    # Set XML Values
    head = people_headers.replace("{{Target}}", target)
    data = people_data.replace("{{searchString}}", restext)
    data = data.replace("{{maxResults}}", str(numresults))
    data = data.replace("{{principalType}}", restype)

    # Build Packet
    p = sr1(IP(dst=destination),data=data,head=head)/TCP()/%s/%s) % (head, data)

    # I probably want to use scapy to form my packet/request...
    # TODO: Use subprocess to launch custom requests through scapy...

# Unit Tests...
people_enum("http://0rigen.net", "text", 20, "All")