from Target import Target

""" Defines an Engagement top-level class

"""


class Engagement:
    """ Defines a Target instance for this engagement

    Every engagement has 1-to-1 target relationship, so the Target will be defined
    when an engagement is created.
    """

    # Function definitions
    def __init__(self):

        # Create target for this engagement
        target = Target()
        target.url = raw_input("[?] Target URL:")
        try:
            target.port = int(raw_input("[?] Target Port:"))
        except ValueError:
            print ("[!] Port must be a number, dummy!")

        # verify that an SP exists at the given URL
        target.check()
        target.id_version()
        print target.sp_version

    # Engagement globals
    auth_type = None  # cookie, userpass, or none
    session_established = False  # boolean

    def authenticate(self, type, cookie=None, user=None, pasw=None):
        print("authenticate")
        # call the Authentication.py module and send along whatever paremeters I got
