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
        self.create_cookie_jar()
        session = requests.Session()
        session.get(self.url, cookies=self.jar)
        return session

    def build_ntlm_session(self):
        self.user = user
        self.paswd = paswd
        session = requests.Session()
        session.auth = (self.user, self, paswd)
        return session

    def create_cookie_jar(self):
        self.jar = cookielib.MozillaCookieJar()
        self.jar.load(self.cookie_file, ignore_discard=True, ignore_expires=True)
