import argparse
import logging
import sys
import user_id
import brute_browse
import url_processor

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"

# TODO: Move functionality calls outside of if statements and into their own functions

def banner():
    print("""
      ___   _                         ___
     / __| | |_    __ _   _ _   ___  | _ \ __ __ __  _ _
     \__ \ | ' \  / _` | | '_| / -_) |  _/ \ V  V / | ' \\
     |___/ |_||_| \__,_| |_|   \___| |_|    \_/\_/  |_||_|  V.01

    SharePoint Security Auditing by @_0rigen / 0rigen.net""")


def changetarget():
        t = raw_input("[!] Please enter a target URL now: ")
        tar = url_processor.checkhttp(t)
        return tar


########################
# Brute Force Browsing #
########################
def bruteforcebrowsing():
    print ("\nBeginning brute force browsing...\n")
    finds = brute_browse.geturlcode(target, None, "service_list.txt")
    print ("\n")
    # TODO: Clean up how 'finds' is printed to make it more easily readable
    print ("I found"),
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


def showmenu():
    while True:
        print("\nPlease choose an option below\n")
        print("[B]rute Force Browsing")
        print("[S]ervice Access Testing")
        print("[P]eople Service Enumeration")
        print("[U]serID Brute Force Search")
        print("[T]arget (Change your target URL)")
        print("[O]utput Redirection (print to files)")
        print("[Q]uit and go home")
        choice = raw_input("# >  ")
        if choice.capitalize() =='B':
            bruteforcebrowsing()
        elif choice.capitalize() =='S':
            print("\nNot yet implemented\n")
        elif choice.capitalize() =='P':
            pickerenumeration()
        elif choice.capitalize() =='U':
            useridenumeration()
        elif choice.capitalize() =='T':
            changetarget()
        elif choice.capitalize() =='O':
            print("\nNot yet implemented\n")
        elif choice.capitalize() =='Q':
            print("Quitting!")
            sys.exit(0)

try:
    # Parse arguments
    # TODO: Investigate turning arguments into long words, but allowing abbreviation instead of requiring it
    parser = argparse.ArgumentParser()
    parser.add_argument("-target", type=str, help="URL of the target SP site")
    parser.add_argument("-b", help="Perform Brute-Force Browsing", action='store_true')
    parser.add_argument("-p", help="Perform Enumeration via Picker Service", action='store_true')
    parser.add_argument("-u", help="Perform Brute-Force User ID Search", action='store_true')
    # TODO: Add command line argument to set the debug level
    # TODO: Handle file output throughout program (probably should be a final clean-up item)
    #parser.add_argument("-o", help="Specify output file", type=argparse.FileType('w'))
    args = parser.parse_args()
    target = args.target

    # Handle stdout redirection for output file
    #if args.o is not None:
    #    sys.stdout = open(args.o.name, 'w')

    # Error if no target specified
    if target is None:
        target = changetarget()

    # Welcome to SharePwn
    banner()

    # Set Logging level (based on command line arg in the future
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    ########################
    # Brute-Force Browsing #
    ########################
    # TODO: Verify Brute-Force Browsing results via manual POST requests to services
    if args.b is True:
        bruteforcebrowsing()

    ######################
    # Picker Enumeration #
    ######################
    # TODO: Create Picker enumeration in people_enum.py
    if args.p is True:
        pickerenumeration()

    ######################
    # UserID Enumeration #
    ######################
    # TODO: Find a way to display these input options better, or allow users to do it form command line -u argument
    if args.u is True:
        useridenumeration()

    # At this point, no arguments were added besides the target, so show the menu
    showmenu()

#####################
# Handle Exceptions #
#####################
except KeyboardInterrupt:
    print("\n\nYour keys interrupted meh! Quitting...")
    sys.exit(0)
except:
    print("Unknown error; iunno d00d...")
    sys.exit(1)
