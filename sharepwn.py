import argparse
import logging
import sys

import brute_browse
import url_processor
import user_id

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"

# TODO: Move functionality calls outside of if statements and into their own functions

# ************************************
# Begin function definitions section
# ************************************
def banner():
    print(chr(27) + "[2J")
    print("""
      ___   _                         ___
     / __| | |_    __ _   _ _   ___  | _ \ __ __ __  _ _
     \__ \ | ' \  / _` | | '_| / -_) |  _/ \ V  V / | ' \\
     |___/ |_||_| \__,_| |_|   \___| |_|    \_/\_/  |_||_|  V.01

    SharePoint Security Auditing by @_0rigen / 0rigen.net""")


################################
# The target is a couplet of   #
# URL and port number, like    #
# [yahoo.com, 443]             #
# return array tarout[]        #
################################
def changetarget():
    tarout = []
    t = raw_input("[?] Please enter a target URL now: ")
    tarout.append(t)
    tarout.append(changeport())  # Call changeport() to get a new port #
    tarout[0] = url_processor.checkhttp(tarout[0], tarout[1])  # Process the target string
    return tarout


# Just a little port changing stub to return
# a numeric port value
def changeport():
    port = raw_input("[?] Enter target port (usually 80 or 443): ")
    port = int(port)
    return port

########################
# Brute Force Browsing #
########################
def bruteforcebrowsing():
    print ("\nBeginning brute force browsing...\n")
    finds = brute_browse.geturlcode(target, None, "service_list.txt")
    print ("\n")
    # TODO: Clean up how 'finds' is printed to make it more easily readable
    print ("I found "),
    print finds


######################
# Picker Enumeration #
######################
def pickerenumeration():
    print ("picker stuff")


#######################
# User ID Enumeration #
#######################
def useridenumeration():
    b = True

    while b is True:
        try:

            mini = raw_input("\r[?] Starting UserID: ")     # Make sure they're integers
            mini = int(mini)
            maxi = raw_input("[?] Ending UserID: ")
            maxi = int(maxi)

            if (mini - maxi) > 0:                           # Make sure they are ordered properly
                sys.stdout.flush()
                print("\n[X] Starting UserID must be less than Ending UserID")
            else:
                b = False                                   # All tests pass

        except:
            sys.stdout.flush()
            print("\n[X] UserIDs must be numeric values only")

    print ("\nBrute-Forcing User IDs...\n")                 # Start working...
    user_id.enumusers(target, mini, maxi)


def showmenu(tar):
    while True:
        print("\n[*] Targeting: %s:%s [*]" % (tar[0], tar[1]))
        print("Please choose an option below: \n")
        print("[B]rute Force Browsing")
        print("[S]ervice Access Testing")
        print("[P]icker Service Enumeration")
        print("[U]serID Brute Force Search")
        print("[T]arget (Change your target URL/Protocol)")
        print("[O]utput Redirection (Print to a file)")
        print("[Q]uit and go home")
        choice = raw_input("Command: ")
        if choice.capitalize() =='B':
            bruteforcebrowsing()
        elif choice.capitalize() =='S':
            print("\nNot yet implemented\n")
        elif choice.capitalize() =='P':
            pickerenumeration()
        elif choice.capitalize() =='U':
            useridenumeration()
        elif choice.capitalize() =='T':
            tar = changetarget()
        elif choice.capitalize() =='O':
            print("\nNot yet implemented\n")
        elif choice.capitalize() =='Q':
            print("Quitting!")
            sys.exit(0)


# ************************************
# Begin instruction section
# ************************************
try:
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

    # Runtime target holder
    target = []

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

    # Welcome to SharePwn
    banner()

    # Set Logging level (based on command line arg in the future
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

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

    # Either no command-line functions were specified or their runs have completed.  Go back to the menu...
    showmenu(target)

#####################
# Handle Exceptions #
#####################
except KeyboardInterrupt:
    print("\n\n[!] Caught keyboard interrupt.  Bye?")
    sys.exit(0)
except:
    print("[X] Unknown error")
    sys.exit(1)
