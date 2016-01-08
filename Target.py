import logging

import URL_Processor
import requests
from Printer import Printer


# import brute_browse


class Target:
    url = None  # target url
    port = None  # target port
    sp_version = None  # SharePoint version number string
    server_version = None  # Server version string
    asp_version = None  # ASP version string
    health_score = None  # SP Health Score
    two_pages = []  # pages that returned a 2xx status code
    four_pages = []  # pages that returned a 4xx status code
    other_pages = []  # pages that returned anything else

    def __init__(self):
        self.url = ''
        self.port = ''
        logging.debug("Target object initialized.")

        self.printer = Printer()

        self.url = self.printer.input("Target URL:")
        logging.debug("Engagement:__init__() got Target URL %s" % self.url)
        try:
            self.port = int(self.printer.input("Target Port:"))  # Turn port input into int
            logging.debug("Engagement:__init__() got Port %d" % self.port)
        except ValueError:
            self.printer.error("Port must be a number")

    # check that a url appears to be a valid SP site
    def check(self):
        self.url = URL_Processor.checkhttp(self.url, self.port)
        logging.info("Target:Check() Processed URL")
        try:
            r = requests.get(self.url, verify=False)
            logging.debug("Target:Check() Requested URL, got code %s" % r.status_code)
            head_check = str(r.headers['microsoftsharepointteamservices'])
            logging.debug("Target:Check() Returning %s as header result" % head_check)
            return head_check
        except:
            logging.error("Target:Check() No sharepoint header found during check(), returning None.")
            return None

    def id_version(self):
        # Request the page
        # HTTPS connections fail if there's a redirect, so just take the first response.
        # HTTP connections are ok with redirects, so they are flagged to allow, with allow_redirects=True
        # User agent needs to be spoofed, since some sites will ignore a 'python' user agent
        if self.port == 443:
            logging.debug("Target:id_version() Requesting with spoofed user-agent on 443")
            r = requests.head(self.url, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'},
                              verify=False)
        elif self.port == 80:
            logging.debug("Target:id_version() Requesting with spoofed user-agent on 80")
            r = requests.head(self.url, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'},
                              allow_redirects=True)

        # Check for a successful response.  Even redirection still contains the necessary headers
        if str(r.status_code).startswith("4") or str(r.status_code).startswith("5"):
            logging.debug("Target:id_version() Version ID failed; Got a response %s" % str(r.status_code))
            return "Unknown"

        # Search for version info in headers
        # SP
        if r.headers.__contains__("microsoftsharepointteamservices"):
            self.sp_version = r.headers['microsoftsharepointteamservices']
        else:
            logging.info("No SP version identified.")

        # ASP
        if r.headers.__contains__("x-aspnet-version"):
            self.asp_version = r.headers['x-aspnet-version']
        else:
            logging.info("ASP version ID failed; successful request but no version information found.")

        # Server
        if r.headers.__contains__("server"):
            self.server_version = r.headers['server']
        else:
            logging.info("Server version ID failed; successful request but no version information found.")

        # Health Score
        if r.headers.__contains__("x-sharepointhealthscore"):
            self.health_score = r.headers['x-sharepointhealthscore']
        else:
            logging.info("Health Score retrieval failed.")

        # Process SharePoint version
        if self.sp_version is None:  # No version info returned
            logging.info("Version ID failed; successful request but no SP version information found.")
        else:
            ver = str(self.sp_version)  # Store the version info and return
            # SP Versions are identified in the response headers as 'MicrosoftSharePointTeamServices': 'X.X.X.X'
            # Identify SP versions via initial GET request
            # 2010 will start with 14, like 14.0.0.6010
            # 2013 will start with 15.
            # 2007 will start with 12.
            # 2003 will start with 6.
            if ver.startswith("6"):
                self.sp_version += ", SharePoint 2003"
            elif ver.startswith("14"):
                self.sp_version += ", SharePoint 2010"
            elif ver.startswith("12"):
                self.sp_version += ", SharePoint 2007"
            elif ver.startswith("15"):
                self.sp_version += ", SharePoint 2013"
            else:
                self.sp_version = " ".join("Unknown SharePoint Version")
            logging.info("SP Version ID successful. Found %s" % self.sp_version)

            # def brute_browse(self):
            # two_pages = brute_browse.geturl_list(self.url, browse_list.txt)
