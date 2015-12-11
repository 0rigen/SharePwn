import logging
import os
import sys

import brute_browse
import people_enum
import url_processor
import user_id
import version_id

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"

red = "\033[31m"  # usually for errors, [X] items
cyan = "\033[36m"
yellow = "\033[33m"  # usually for information and requests, the [?] items
green = "\033[92m"  # Information and success, [!]
blue = "\033[94m"
endc = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"


# TODO: Move functionality calls outside of if statements and into their own functions


# ************************************
# Begin function definitions section
# ************************************
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[95m" + bold + """
      ___   _                         ___
     / __| | |_    __ _   _ _   ___  | _ \ __ __ __  _ _
     \__ \ | ' \  / _` | | '_| / -_) |  _/ \ V  V / | ' \\
     |___/ |_||_| \__,_| |_|   \___| |_|    \_/\_/  |_||_|  V.01

    SharePoint Security Auditing by @_0rigen / 0rigen.net""" + endc)


################################
# The target is a couplet of   #
# URL and port number, like    #
# [yahoo.com, 443]             #
# return array tarout[]        #
################################
def changetarget():
    tarout = []
    t = raw_input(cyan + "[?] Please enter a target URL now: " + endc)
    tarout.append(t)
    tarout.append(changeport())  # Call changeport() to get a new port #
    tarout[0] = url_processor.checkhttp(tarout[0], tarout[1])  # Process the target string
    return tarout


# Just a little port changing stub to return
# a numeric port value
def changeport():
    while True:
        try:
            port = raw_input(cyan + "[?] Enter target port (usually 80 or 443): " + endc)
            port = int(port)
            break
        except:
            print(yellow + "[!] Bad Port.  Try again." + endc)
    return port


########################
# Brute Force Browsing #
########################
def bruteforcebrowsing():
    print (yellow + "\n[!] Beginning brute force browsing...\n" + endc)
    finds = brute_browse.geturl_list(target[0], "service_list.txt")
    print ("\n")


def version():
    version_id.identify(target[0], target[1])


######################
# Picker Enumeration #
######################
def peopleenumeration():
    people_enum.people_enum(target, "admin", 1000, "All")


#######################
# User ID Enumeration #
#######################
def useridenumeration():
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
    user_id.enumusers(target, mini, maxi)


def showmenu(tar):
    while True:
        print(endc + blue + "\n[*] Targeting: %s:%s [*]" % (tar[0], tar[1]) + endc)
        print(cyan + "Please choose an option below: \n")
        print("[" + yellow + "V" + endc + cyan + "]ersion Identification")
        print("[" + yellow + "B" + endc + cyan + "]rute Force Browsing")
        print("[" + yellow + "S" + endc + cyan + "]ervice Access Testing")
        print("[" + yellow + "P" + endc + cyan + "]eople Service Enumeration")
        print("[" + yellow + "U" + endc + cyan + "]serID Brute Force Search")
        print("[" + yellow + "T" + endc + cyan + "]arget (Change your target URL/Protocol)")
        print("[" + yellow + "O" + endc + cyan + "]utput Redirection (Print to a file)")
        print("[" + yellow + "Q" + endc + cyan + "]uit and go home")
        choice = raw_input("Command: " + endc)
        if choice.capitalize() == 'V':
            version()
        if choice.capitalize() == 'B':
            bruteforcebrowsing()
        elif choice.capitalize() == 'S':
            print("\nNot yet implemented\n")
        elif choice.capitalize() == 'P':
            peopleenumeration()
        elif choice.capitalize() == 'U':
            useridenumeration()
        elif choice.capitalize() == 'T':
            tar = changetarget()
        elif choice.capitalize() == 'O':
            print("\nNot yet implemented\n")
        elif choice.capitalize() == 'Q':
            print("Quitting!")
            sys.exit(0)


# ************************************
# Begin instruction section
# ************************************
try:
    # Runtime target holder
    target = changetarget()

    # This huge comment block contains command-line parsing code.  This will be implemented in a future version #
    '''
    # Parse arguments
    # TODO: Investigate turning arguments into long words, but allowing abbreviation instead of requiring it
    parser = argparse.ArgumentParser()
    parser.add_argument("-target", type=str, help="URL of the target SP site")
    parser.add_argument("-port", type=str, help="Port/Protocol to target (80 or 443)")
    parser.add_argument("-b", help="Perform Brute-Force Browsing", action='store_true')
    parser.add_argument("-p", help="Perform Enumeration via Picker Service", action='store_true')
    parser.add_argument("-u", help="Perform Brute-Force User ID Search", action='store_true')
    # TODO: Add command line argument to set the debug level
    # TODO: Handle file output throughout program (probably should be a final clean-up item)
    # parser.add_argument("-o", help="Specify output file", type=argparse.FileType('w'))
    args = parser.parse_args()

    ######################################################################################
    # Handle target specification.  This can come in the following combinations:
    # 1; Port but no target
    # 2; target but no port
    # 3; Neither target nor port
    # 4; Both provided
    # Right now, if the target is blank, then both must be set manually, eliminating (2)
    #####################################################################################

    # If the user was nice and provided both target and port #...
    if args.target is not None:
        if args.port is not None:
            target[0] = args.target
            target[1] = args.port
            # If the user provided a target but no port
        elif args.port is None:
            target[1] = changeport()
    # Else, no target was specified, and we handle (1) and (2) as a single case
    else:
        target = changetarget()

    #####################################################################
    # Handle command-line functionality specification.                  #
    # Rather than using the menu, a user can specify functions to use   #
    # via commnad line args.  Here, we catch those args and run the     #
    # corresponding functions.                                          #
    #####################################################################
    # (-b) Brute-Force Browsing #
    # TODO: Verify Brute-Force Browsing results via manual POST requests to services
    if args.b is True:
        bruteforcebrowsing()

    # (-p) Picker Enumeration #
    # TODO: Create Picker enumeration in people_enum.py
    if args.p is True:
        pickerenumeration()

    # (-u) UserID Enumeration #
    # TODO: Find a way to display these input options better, or allow users to do it form command line -u argument
    if args.u is True:
        useridenumeration()

    '''

    # Welcome to SharePwn
    banner()

    # Set Logging level (based on command line arg in the future
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


    # Either no command-line functions were specified or their runs have completed.  Go back to the menu...
    showmenu(target)

#####################
# Handle Exceptions #
#####################
except KeyboardInterrupt:
    print(red + "\n\n[!] Caught keyboard interrupt.  Bye?" + endc)
    sys.exit(0)
except:
    print(red + bold + "\n[X] Unknown error" + endc)
    sys.exit(1)
