import argparse
import logging
import sys
from sys import stdout
import brute_browse

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"


def banner():
    print("""
      ___   _                         ___
     / __| | |_    __ _   _ _   ___  | _ \ __ __ __  _ _
     \__ \ | ' \  / _` | | '_| / -_) |  _/ \ V  V / | ' \\
     |___/ |_||_| \__,_| |_|   \___| |_|    \_/\_/  |_||_|  V.01

    SharePoint Security Auditing by @_0rigen / 0rigen.net""")

try:
    # Parse argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-target", type=str, help="URL of the target SP site")
    parser.add_argument("-b", help="Perform Brute-Force Browsing", action='store_true')
    parser.add_argument("-p", help="Perform Enumeration via Picker Service", action='store_true')
    parser.add_argument("-u", help="Perform Brute-Force User ID Search", action='store_true')
    parser.add_argument("-o", help="Specify output file", type=argparse.FileType('w'))
    args = parser.parse_args()
    target = args.target

    # Handle stdout redirection for output file
    if args.o is not None:
        print args.o
        sys.stdout = open(args.o.name, 'w')

    # Error if no target specified
    if target is None:
        print("No target specified.  Use -t to specify the target URL")
        sys.exit(1)

    else:
        # Welcome to SharePwn
        banner()

        # Set Logging level (based on command line arg in the future
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

        if args.b is True:
            print ("\nBeginning brute force browsing...")
            finds = brute_browse.geturlcode(target, None, "service_list.txt")
            print ("\n")
            print ("I found"),
            print finds
        if args.p is True:
            print ("\nEnumerating users via Picker service...")
        if args.u is True:
            print ("\nBrute-Forcing User IDs...")

except KeyboardInterrupt:
    print("\n\nYour keys interrupted meh! Quitting...")
    sys.exit(0)
except:
    print("Unknown error; iunno d00d...")
    sys.exit(1)


