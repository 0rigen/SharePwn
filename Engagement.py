import logging

from Authenticator import Authenticator
from Target import Target

""" Defines an Engagement top-level class

"""


class Engagement:
    """ Defines a Target instance for this engagement

    Every engagement has 1-to-1 target relationship, so the Target will be defined
    when an engagement is created.
    """

    # Engagement globals
    target = None
    authenticator = None
    auth_type = None  # cookie, userpass, or none
    session_established = False  # boolean
    session = None  # Session object

    def __init__(self):
        """ Initialize the Engagement

        """
        self.target = Target()  # Create the target

        # Get the target
        self.target.url = raw_input("[?] Target URL:")
        logging.debug("Engagement:__init__() got Target URL %s" % self.target.url)
        try:
            self.target.port = int(raw_input("[?] Target Port:"))  # Turn port input into int
            logging.debug("Engagement:__init__() got Port %d" % self.target.port)
        except ValueError:
            print ("[!] Port must be a number")

        # Create authenticator
        self.authenticator = Authenticator()  # Create authenticator for this engagement
        logging.info("Engagement object initialized.")

        # Set up authentication
        self.auth_type = raw_input("[?] Authenticate with a (C)ookie, (N)TLM, or remain (A)nonymous?")
        if self.auth_type.startswith("C"):
            self.authenticator.cookie_file = raw_input("[?] Full path to cookie file: ")
            logging.debug("Got cookie location as %s" % self.authenticator.cookie_file)
            self.authenticator.build_cookie_session()
        if self.auth_type.startswith("N"):
            self.authenticator.user = raw_input("[?] Username: ")
            self.authenticator.paswd = raw_input("[?] Password: ")
            self.authenticator.build_ntlm_session()
        if self.auth_type.startswith("A"):
            pass

        # Verify SP exists at given location and find the version
        logging.debug("Engagement:__init__() calling Target:check()")
        self.target.check()  # Check that SP exists at given url
        # TODO Handle the case where SP is not present or not found
        logging.debug("Engagement:__init__() calling Target:id_version()")
        self.target.id_version()  # ID the SP version in use
