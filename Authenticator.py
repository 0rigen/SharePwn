import cookielib
import logging

import requests

# Disable HTTPS cert warnings
requests.packages.urllib3.disable_warnings()


class Authenticator:
    """ Authenticator handles building sessions based on any available authentication types

    """
    type = None  # cookie, ntlm, or None
    user = None
    paswd = None
    cookie_file = None
    jar = None
    url = None

    # Function definitions
    def __init__(self):
        self.data = []
        logging.debug("Authentication Object Initialized.")

    def build_cookie_session(self):
        logging.debug("Authenticator Cookie Session being built...")
        try:
            self.create_cookie_jar()
            session = requests.Session()
            session.get(self.url, cookies=self.jar)
            return session
        except:
            logging.debug("Authenticator Cookie Session Failed.")
            return None

    def build_ntlm_session(self):
        logging.debug("Authenticator NTLM Session being built...")
        try:
            self.user = user
            self.paswd = paswd
            session = requests.Session()
            session.auth = (self.user, self, paswd)
            return session
        except:
            logging.debug("Authenticator NTLM Session Failed.")
            return None

    def create_cookie_jar(self):
        logging.debug("Authenticator Cookie Jar being created...")
        try:
            self.jar = cookielib.MozillaCookieJar()
            self.jar.load(self.cookie_file, ignore_discard=True, ignore_expires=True)
        except:
            logging.debug("Cookie Jar Creation Failed.")
            return None
