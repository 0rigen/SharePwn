import sys

from Engagement import Engagement

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Development"

# TODO: Finish Authentication via cookies
# TODO: Add timeout to requests to prevent hangs

# Begin instruction section
# ************************************
try:
    # Create new engagement object
    my_engagement = Engagement()

    # TODO: Find a way to dynamically build functionality around the user-defined extension modules
    # For now, I will hardcode the functionality that exists, and can include more modules manually later on

    # Show the Engagement menu
    # TODO: Is there a better place to put these function handlers?
    while True:
        menu_choice = my_engagement.printer.show_menu()
        if menu_choice.startswith('Q'):
            my_engagement.printer.error("Quitting...")
            sys.exit(0)
        elif menu_choice.startswith('V'):
            print "\r"
            my_engagement.printer.status("SharePoint Version: " + str(my_engagement.target.sp_version))
            my_engagement.printer.status("Server Software: " + str(my_engagement.target.server_version))
            my_engagement.printer.status("ASP.NET Version: " + str(my_engagement.target.asp_version))
            print "\r"
        elif menu_choice.startswith('B'):
            my_engagement.printer.status(
                    "I want to brute browse, but I don't know how to call a dynamically imported module...")


# Handle Exceptions
except KeyboardInterrupt:
    my_engagement.printer.error("Caught keyboard interrupt!")
    sys.exit(0)
except:
    my_engagement.printer.error("Unknown error")
    sys.exit(1)
