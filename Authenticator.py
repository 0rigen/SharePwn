import cookielib
import logging

# from requests_ntlm import HttpNtlmAuth # TODO Fix this import - its broken
# from requests.auth import HTTPDigestAuth
import requests
from Printer import Printer
from Target import Target

# Disable HTTPS cert warnings
requests.packages.urllib3.disable_warnings()


# TODO: What do I need to do here for HTTP?  It's authenticated per-request, isn't it?
class Authenticator:
    """ Authenticator handles building sessions based on any available authentication types

    """
    type = None  # Cookie, NTLM, HTTP_Basic, HTTP_Digest, or None
    user = None
    paswd = None
    domain = None
    cookie_file = None
    jar = None
    url = None
    cookie_dict = None  # actual string of cookies to include in requests
    printer = None

    # Function definitions
    def __init__(self):
        self.data = []
        logging.debug("Authentication Object Initialized.")
        printer = Printer()

        # Set up authentication for the engagement
        engagement.auth_type = printer.input(
                "Authenticate with a (C)ookie, (N)TLM, (S)imple HTTP, (D)igest, or remain [Anonymous]?")
        if engagement.auth_type.startswith("C"):
            self.cookie_file = printer.input("Full path to cookie file: ")
            logging.debug("Got cookie location as %s" % self.cookie_file)
            self.build_cookie_session()
        elif engagement.auth_type.startswith("N"):
            self.user = printer.input("Username: ")
            self.paswd = printer.input("Password: ")
            self.build_ntlm_session()
        elif engagement.auth_type.startswith("D"):
            self.user = printer.input("Username: ")
            self.paswd = printer.input("Password: ")
            self.build_http_digest()
        elif engagement.auth_type.startswith("S"):
            self.user = printer.input("Username: ")
            self.paswd = printer.input("Password: ")
            self.build_http_basic()
        elif engagement.auth_type.startswith("A"):
            pass
        else:
            pass

    def build_cookie_session(self):
        logging.debug("Authenticator Cookie Session being built...")
        try:
            self.type = "Cookie"
            self.create_cookie_jar()
            session = requests.Session()
            session.get(self.url, cookies=self.jar)
            return session
        except:
            logging.debug("Authenticator Cookie Session Failed.")
            return None

    def build_ntlm_session(self, user, paswd):
        logging.debug("Authenticator NTLM Session being built...")
        try:
            self.type = "NTLM"
            self.user = user
            self.paswd = paswd
            session = requests.Session()
            self.printer.error("****NTLM Broken - the import needs fixed! It's a TODO item!*****")
            # session.auth = HttpNtlmAuth(self.user, self.paswd, session)
            session.get(Target.url)
            return session
        except:
            logging.debug("Authenticator NTLM Session Failed.")
            return None

    def build_http_basic(self, user, paswd):
        logging.debug("Authenticator HTTP Basic Requested.")
        self.type = "HTTP_Basic"
        self.user = user
        self.paswd = paswd
        # TODO Is there anything else to do for HTTP Basic?

    def build_http_digest(self, user, paswd):
        logging.debug("Authenticator HTTP Digest Requested.")
        self.type = "HTTP_Digest"
        self.user = user
        self.paswd = paswd
        # get_args = Target.url + ", auth=HTTPDigestAuth('" + self.user + "', '" + self.paswd + "'))"
        # requests.get(get_args)  # Perform an initial get in order to get the servers opaque directive

    def create_cookie_jar(self):
        logging.debug("Authenticator Cookie Jar being created...")
        try:
            self.jar = cookielib.MozillaCookieJar()
            self.jar.load(self.cookie_file, ignore_discard=True, ignore_expires=True)
        except:
            logging.debug("Cookie Jar Creation Failed.")
            return None
