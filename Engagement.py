import importlib
import logging
import os
import sys

from Printer import Printer
from Target import Target

""" Defines an Engagement top-level class
 * load_modules will import any .py script found in the SharePwn/modules/ directory

"""

# Globals?
dynamic_modules = []


class Engagement:
    """ Defines a Target instance for this engagement

    Every engagement has 1-to-1 target relationship, so the Target will be defined
    when an engagement is created.
    """

    # Engagement globals
    printer = None
    target = None
    authenticator = None
    auth_type = None  # cookie, userpass, or none
    session_established = False  # boolean
    session = None  # Session object

    def __init__(self):
        """ Initialize the Engagement

        """
        self.printer = Printer()  # Create the printer
        self.load_modules()  # Load modules from modules/ directory
        self.target = Target()  # Create the target

        # Get the target
        self.target.url = self.printer.input("Target URL:")
        logging.debug("Engagement:__init__() got Target URL %s" % self.target.url)
        try:
            self.target.port = int(self.printer.input("Target Port:"))  # Turn port input into int
            logging.debug("Engagement:__init__() got Port %d" % self.target.port)
        except ValueError:
            self.printer.error("Port must be a number")


        # Verify SP exists at given location and find the version
        logging.debug("Engagement:__init__() calling Target:check()")
        self.target.check()  # Check that SP exists at given url
        # TODO Handle the case where SP is not present or not found
        logging.debug("Engagement:__init__() calling Target:id_version()")
        self.target.id_version()  # ID the SP version in use

    def load_modules(self):
        logging.debug("Importing modules/ ...")
        try:
            module_list = os.listdir("modules")
            for item in module_list:
                # Load .py scripts as long as it's not the __init__ script
                if item.startswith("__init__") is False and item.endswith(".py") is True:
                    logging.debug("Found module: %s" % item)
                    p, m = item.split('.', 1)
                    dynamic_modules.append(p)
                    mod_name = "modules." + p
                    logging.debug("Importing %s" % mod_name)
                    importlib.import_module(mod_name)
            self.printer.status("Loaded Modules: ")
            for i in range(0, int(dynamic_modules.__len__())):
                print dynamic_modules[i] + ", ",
            print "\n"
        except:
            sys.stdout.flush()
            self.printer.error("Failed to Load SharePwn modules from SharePwn/modules/ directory.")
