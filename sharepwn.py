import os
import sys

import requests
from Engagement import Engagement

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Development"

# Let's suppress unverified HTTPS warnings...
requests.packages.urllib3.disable_warnings()

# Colors for terminal output
red = "\033[31m"  # usually for errors, [X] items
cyan = "\033[36m"
yellow = "\033[33m"  # usually for information and requests, the [?] items
green = "\033[92m"  # Information and success, [!]
blue = "\033[94m"
endc = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"


# TODO: Add Authentication via cookies
# TODO: Add timeout to requests to prevent hangs


# ************************************
# Begin function definitions section
# ************************************


################################
# Show the SharePwn banner     #
################################
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[95m" + bold + """
      ___   _                         ___
     / __| | |_    __ _   _ _   ___  | _ \ __ __ __  _ _
     \__ \ | ' \  / _` | | '_| / -_) |  _/ \ V  V / | ' \\
     |___/ |_||_| \__,_| |_|   \___| |_|    \_/\_/  |_||_|  BETA

    SharePoint Security Auditing by @_0rigen / 0rigen.net""" + endc)


"""
########################
# Brute Force Browsing #
########################
def bruteforcebrowsing(target):
    print (yellow + "\n[!] Beginning brute force browsing...\n" + endc)
    finds = brute_browse.geturl_list(target, "browse_list.txt")  # Brute force and save results
    print ("\n")


##########################
# Version Identification #
##########################
def version(target):
    version_id.identify(target[0], target[1])


######################
# People Enumeration #
######################
def peopleenumeration(target, creds):
    if type(creds) is list:
        people_enum.creds_search(target, creds)
    elif isinstance(creds, cookielib.LWPCookieJar):
        people_enum.cookie_search(target, creds)
    elif creds is None:
        people_enum.anon_search(target)


#######################
# User ID Enumeration #
#######################
def useridenumeration(target):
    b = True

    while b is True:
        try:

            mini = raw_input(yellow + "\r[?] Starting UserID: " + endc)  # Make sure they're integers
            mini = int(mini)
            maxi = raw_input(yellow + "[?] Ending UserID: " + endc)
            maxi = int(maxi)

            if (mini - maxi) > 0:  # Make sure they are ordered properly
                sys.stdout.flush()
                print(red + "\n[X] Starting UserID must be less than Ending UserID" + endc)
            else:
                b = False  # All tests pass

        except:
            sys.stdout.flush()
            print(red + "[X] UserIDs must be numeric values only" + endc)

    print (green + "\n[!] Brute-Forcing User IDs...\n" + endc)  # Start working...
    FoundUsers = user_id.enumusers(target, mini, maxi)
    if FoundUsers.__len__() != 0:
        print (yellow + "[*] Users found:\n" + endc)
        for user in FoundUsers:
            print user,
    else:
        print(yellow + "[*] No users were found :(" + endc)
"""


###################################
# Show the menu                   #
# @tar - the target, port couplet #
###################################
def showmenu():
    while True:
        print(cyan + "Please choose an option below: \n")
        print("[" + yellow + "V" + endc + cyan + "]ersion Identification")
        print("[" + yellow + "B" + endc + cyan + "]rute Force Browsing")
        # print("[" + yellow + "S" + endc + cyan + "]ervice Interrogater")
        print("[" + yellow + "P" + endc + cyan + "]eople Service Enumeration")
        print("[" + yellow + "U" + endc + cyan + "]serID Brute Force Search")
        print("[" + yellow + "A" + endc + cyan + "]uthentication Configuration")
        print("[" + yellow + "T" + endc + cyan + "]arget (Change your target URL/Protocol)")
        # print("[" + yellow + "O" + endc + cyan + "]utput Redirection (Print to a file)")
        print("[" + yellow + "Q" + endc + cyan + "]uit and go home")
        choice = raw_input("Command: " + endc)
        if choice.capitalize() == 'V':
            version(tar)
        elif choice.capitalize() == 'B':
            bruteforcebrowsing(tar)
        # elif choice.capitalize() == 'S':
        #    service_interrogator.submenu(tar)
        elif choice.capitalize() == 'P':
            peopleenumeration(tar, auth_type)
        elif choice.capitalize() == 'U':
            useridenumeration(tar)
        elif choice.capitalize() == 'A':
            auth_type = authentication_config()
        elif choice.capitalize() == 'T':
            tar = changetarget(True)
        # elif choice.capitalize() == 'O':
        #    print("\nNot yet implemented\n")
        elif choice.capitalize() == 'Q':
            print(yellow + "[*]" + endc + " Shutting down...")
            sys.exit()
        else:
            print(yellow + bold + "[!] Command not understood; try again, buddy!" + endc)


# ************************************
# Begin instruction section
# ************************************
try:
    # Create new engagement object
    my_engagement = Engagement()

    # Welcome to SharePwn
    # print("Target: %s" % my_engagement.target.url),
    # print("on port %s" % str(my_engagement.target.port))
    banner()

    # Either no command-line functions were specified or their runs have completed.  Go back to the menu...
    showmenu()

#####################
# Handle Exceptions #
#####################
except KeyboardInterrupt:
    print(red + bold + "\n\n[!] Caught keyboard interrupt.  Bye?" + endc)
    sys.exit(0)
except:
    print(red + bold + "\n[X] Unknown error" + endc)
    sys.exit(1)
