import argparse
import cookielib
import logging
import os
import sys

import brute_browse
import people_enum
import requests
import url_processor
import user_id
import version_id

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


# TODO: Add Authentication attempts via "from requests_ntlm import HttpNtlmAuth"
# TODO: Add Authentication via cookies
# TODO: Explore moving my web requests into a single function rather than being spread throughout the program
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


###################################################
# Configures either NTLM or Cookie authentication #
# ntlm - return a couple of username:password     #
# cookie - return a ful path of the cookie file?? #
###################################################
def authentication_config():
    while True:
        type = str(raw_input(
                yellow + "[!]" + endc + " Use " + green + "(N)" + endc + "TLM or " + blue + "(C)" + endc + "ookie authentication?"))

        # NTLM Authentication Credentials
        if type.capitalize().startswith("N"):
            username = raw_input(blue + "Username: " + endc)
            password = raw_input(blue + "Password: " + endc)
            print(yellow + "[*]" + endc + " Using credentials " + green + "%s:%s" + endc) % (
                str(username), str(password))
            ntlm = [username, password]
            return ntlm

        # Cookie-based Authentication
        elif type.capitalize().startswith("C"):
            lwp_cj = cookielib.LWPCookieJar()
            # This will likely use the CookieJar package to handle the cookies... I can either have the user
            # Load the cookies entirely from a file, or I can even capture HTTP responses and set cookies
            # as instructed, using extract_cookies().
            # Alternatively, FileCookieJar can read and save to file, but an existing file has to be in the correct
            # format for that to work.
            # https://docs.python.org/2/library/cookielib.html
            cookie_file = raw_input(blue + "Cookie File Location: " + endc)
            print(yellow + "[*]" + endc + " Loading cookie from %s" % str(cookie_file))
            cookie_file = str(cookie_file)
            try:
                lwp_cj.load(cookie_file, ignore_discard=True, ignore_expires=True)
                print(green + "[*]" + endc + " Cookies loaded into CookieJar, We're ready to go!")
                return lwp_cj
            except:
                print(red + "[!] " + endc + "Failed to load cookie.")
                break
                # session = requests.session(cookies=cookies)
                # The above line needs to go into the request location


##################################################
# check that a url appears to be an SP site      #
# by checking the headers                        #
# @target the target url and port                #
##################################################
def check(target):
    url = url_processor.checkhttp(target[0], target[1])
    try:
        r = requests.get(url, verify=False)
        head_check = str(r.headers['microsoftsharepointteamservices'])
        return head_check
    except:
        print (red + "[!] " + endc + "No SharePoint found at the given URL.  Check your URL and port specification.")
        return None


#############################################################
# The target is a couplet of URL and port number,           #
#       like [yahoo.com, 443]                               #
# @full - boolean specifying a full change - this is        #
# necessary to handle the various command line combinations #
# as well as a full change during runtime                   #
# return array tarout[]                                     #
#############################################################
def changetarget(full):
    # If the full flag is True, just erase the existing Target[] for simplicity
    if full:
        target[0] = None
        target[1] = None

    # Do the changes
    while True:

        tarout = ["", ""]
        t = raw_input(cyan + "[?] Please enter a target URL now: " + endc)
        tarout[0] = t
        target[0] = t  # Put on global var...cause I gotta

        # First run: No port set, and full = False
        if full is not True and target[1] is None:
            tarout[1] = changeport()

        # Runtime change: Full is true and port has been cleared
        elif full is True and target[1] is None:
            tarout[1] = changeport()  # Call changeport() for runtime change

        # If we were just here to get a url, but the port was specified...
        elif full is not True and target[1] is not None:
            tarout[1] = target[1]

        # If we get here, likely the user failed to specify a valid URL the first time and we're rewriting target[]
        else:
            tarout[1] = changeport()

        # Assign that new port to the global variable
        target[1] = tarout[1]

        tarout[0] = url_processor.checkhttp(t, tarout[1])  # Process the target string

        if check(tarout) is not None:
            # With the new port, go ahead and correct the target specification for the protocol
            return tarout

        else:
            # Loop again, but set full to True, b/c we need to overwrite what was previously specified.
            full = True
            continue


# Just a little port changing stub to return
# a numeric port value
##########################################################
# changeport() requests and validates a user-defined port #
# @port - the numeric port value                         #
##########################################################
def changeport():
    while True:
        try:
            port = raw_input(cyan + "[?] Enter target port (80 or 443): " + endc)
            port = int(port)
            if port == 80 or 443:
                break
        except:
            print(yellow + "[!] Bad Port.  Try again." + endc)

    # Check for a standard port number
    var = url_processor.checkhttp(target[0], port)
    if var is not None:
        target[1] = var
    # If a non standard port was identified, call self
    else:
        port = changeport()

    return port


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


################################################################################
# showtarget() - displays target and credentials being used                    #
# @tar - the target url                                                        #
# @auth - the authentication object (either a user/pass couplet or a cookiejar #
################################################################################
def showtarget(tar, auth):
    print(endc + blue + "\n[*] Targeting: %s:%s [*]" % (tar[0], tar[1]) + endc)
    if auth is None:
        print(endc + blue + "[*] Testing as an Unauthenticated user" + endc)
    elif isinstance(auth, cookielib.LWPCookieJar):
        print(endc + blue + "[*] Using Saved Cookie Jar [*]")
    elif type(auth) is list:
        print(endc + blue + "[*] Authenticating as " + green + "%s:%s" + endc) % (str(auth[0]), str(auth[1]))


###################################
# Show the menu                   #
# @tar - the target, port couplet #
###################################
def showmenu(tar):
    auth_type = None
    while True:
        showtarget(tar, auth_type)
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
    # Runtime target holder
    target = [None, None]
    par_cookie = None
    par_credentials = None

    # Welcome to SharePwn
    banner()

    # Parse arguments
    # TODO: Investigate turning arguments into long words, but allowing abbreviation instead of requiring it
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=str, help="URL of the target SP site")
    parser.add_argument("-p", type=str, help="Port/Protocol to target (80 or 443)")
    parser.add_argument("-v", help="Perform Version Detection", action='store_true')
    parser.add_argument("-b", help="Perform Brute-Force Browsing", action='store_true')
    parser.add_argument("-pe", help="Perform Enumeration via People Service", action='store_true')
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

    # A Target was provided
    if args.t is not None:
        # A port was also provided
        if args.p is not None:
            target[0] = args.t  # Assign values
            target[1] = int(args.p)
            target[0] = url_processor.checkhttp(target[0], target[1])  # check URL

        # If the user provided a target but no port
        elif args.p is None:
            print(red + "[!]" + " Target specified on command line, but no port!  Use -p to specify the port!")
            sys.exit(0)

    # No Target was provided...
    elif args.t is None:
        # A port was provided, but no target
        if args.p is not None:
            print(red + "[!]" + " Port specified on command line, but no target!  Use -t to specify the target!")
            sys.exit(0)

        # Nothing was provided...
        elif args.p is None:
            target = changetarget(False)

    # error case... should never go this route
    else:
        print("This case should never have been reached... 0x01")

    #####################################################################
    # Handle command-line functionality specification.                  #
    # Rather than using the menu, a user can specify functions to use   #
    # via commnad line args.  Here, we catch those args and run the     #
    # corresponding functions.                                          #
    #####################################################################
    # (-v) Version Detection #
    if args.v is True:
        version_id.identify(target[0], target[1])

    # (-b) Brute-Force Browsing #
    if args.b is True:
        bruteforcebrowsing(target)

    # (-p) Picker Enumeration #
    if args.pe is True:
        peopleenumeration(target)

    # (-u) UserID Enumeration #
    # TODO: Find a way to display these input options better, or allow users to do it form command line -u argument
    if args.u is True:
        useridenumeration(target)

    # Set Logging level (based on command line arg in the future
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    # Either no command-line functions were specified or their runs have completed.  Go back to the menu...
    showmenu(target)

#####################
# Handle Exceptions #
#####################
except KeyboardInterrupt:
    print(red + bold + "\n\n[!] Caught keyboard interrupt.  Bye?" + endc)
    sys.exit(0)
except:
    print(red + bold + "\n[X] Unknown error" + endc)
    sys.exit(1)
