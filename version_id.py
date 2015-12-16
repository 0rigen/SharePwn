import logging

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


# TODO Research what difference the version makes to interrogation functions.  The results of this check may impact later requests

####################################################
# identify                                         #
# Record a response from the target and examines   #
# the headers for SP version information           #
# @url - the target                                #
# @ port - the target port                         #
####################################################
def identify(url, port=None):
    # Process the link, if port is specified
    if port is not None:
        link = url_processor.checkhttp(url, port)
    else:
        link = url

    # Request the page
    # HTTPS connections fail if there's a redirect, so jus take the first response.
    # HTTP connections are ok with redirects, so they are flagged to allow.
    if port == 443:
        r = requests.head(link, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'})
    elif port == 80:
        r = requests.head(link, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'},
                          allow_redirects=True)

    # Check for a successful response.  Redirection still contains the necessary headers
    if str(r.status_code).startswith("4") or str(r.status_code).startswith("5"):
        print(
            yellow + "[!] Unsuccessful request when attempting to identify SP version.  Version remains Unknown..." + endc)
        logging.info("Version ID failed; Got a response %s" % str(r.status_code))
        return "Unknown"

    # Search for version info in headers
    # SP
    if r.headers.__contains__("microsoftsharepointteamservices"):
        sp_match = r.headers['microsoftsharepointteamservices']
    else:
        sp_match = None
        logging.info("No SP version identified.")

    # ASP
    if r.headers.__contains__("x-aspnet-version"):
        asp_match = r.headers['x-aspnet-version']
    else:
        asp_match = None
        logging.info("ASP version ID failed; successful request but no version information found.")

    # Server
    if r.headers.__contains__("server"):
        serv_match = r.headers['server']
    else:
        serv_match = None
        logging.info("Server version ID failed; successful request but no version information found.")

    # Health Score
    if r.headers.__contains__("x-sharepointhealthscore"):
        health_match = r.headers['x-sharepointhealthscore']
    else:
        health_match = None
        logging.info("Health Score retrieval failed.")

    # Process SharePoint version
    if sp_match is None:  # No version info returned
        print(yellow + "[!] No SharePoint version information returned." + endc)
        logging.info("Version ID failed; successful request but no SP version information found.")
    else:
        ver = str(sp_match)  # Store the version info and return
        print(green + "\n[*] SharePoint version identified as " + bold + "%s;" % ver + endc),
        logging.info("SP Version ID successful. Found %s" % ver)

        # SP Versions are identified in the response headers as 'MicrosoftSharePointTeamServices': 'X.X.X.X'
        # Identify SP versions via initial GET request
        # 2010 will start with 14, like 14.0.0.6010
        # 2013 will start with 15.
        # 2007 will start with 12.
        # 2003 will start with 6.
        if ver.startswith("6"):
            print(green + bold + "SharePoint 2003" + endc)
        elif ver.startswith("14"):
            print(green + bold + "SharePoint 2010" + endc)
        elif ver.startswith("12"):
            print(green + bold + "SharePoint 2007" + endc)
        elif ver.startswith("15"):
            print(green + bold + "SharePoint 2013" + endc)

    # Process ASP version
    if asp_match is not None:
        ver = str(asp_match)  # Store the version info and return
        print(green + "\n[*] ASP version identified as " + bold + "%s" % ver + endc)
        logging.info("ASP Version ID successful. Found %s" % ver)

    # Process Server version
    if serv_match is not None:
        ver = str(serv_match)  # Store the version info and return
        print(green + "\n[*] Server version identified as " + bold + "%s" % ver + endc)
        logging.info("Server version ID successful. Found %s" % ver)

    # Print Health Score
    if health_match is not None:
        ver = str(health_match)  # Store the version info and return
        print(green + "\n[*] Health Score: " + bold + "%s" % ver + endc)
