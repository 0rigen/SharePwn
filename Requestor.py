import logging

import requests
from Authenticator import Authenticator
from Target import Target

""" Class that handles getting pages and sending info to the SP site


"""


class Requestor:
    # Globals
    auth = None
    arg_string = None

    def __init__(self):
        logging.debug("Requester Object Initialized.")
        self.auth = "None"
        self.arg_string = ""

    def get_it(self, arg_string):
        self.find_type()
        self.construct_request()
        logging.debug("Sending GET")
        r = requests.get(arg_string)
        return r

    def post_it(self, arg_string):
        self.find_type()
        self.construct_request()
        logging.debug("Sending POST")
        r = requests.post(arg_string)
        return r

    def find_type(self):
        self.auth = Authenticator.type
        logging.debug("Requestor auth set from Authenticator Object.")

    def construct_request(self):
        if self.auth is "NTLM":
            self.arg_string = Target.url  # NTLM is already authenticated per session, so not much to see here...
        if self.auth is "Cookie":
            self.arg_string = Target.url + ", cookies=" + Authenticator.cookie_dict + ")"
        if self.auth is "HTTP_Basic":
            self.arg_string = Target.url + ", auth=('" + Authenticator.user + "', '" + Authenticator.paswd + '))'
        if self.auth is "HTTP_Digest":
            self.arg_string = Target.url + ", auth=HTTPDigestAuth('" + Authenticator.user + "', '" + Authenticator.paswd + "'))"
