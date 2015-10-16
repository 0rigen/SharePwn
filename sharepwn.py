import argparse
import logging
import sys
import url_requester

__author__ = '0rigen'


class Engagement:

    def __init__(self):
        print("""
          ___   _                         ___
         / __| | |_    __ _   _ _   ___  | _ \ __ __ __  _ _
         \__ \ | ' \  / _` | | '_| / -_) |  _/ \ V  V / | ' \\
         |___/ |_||_| \__,_| |_|   \___| |_|    \_/\_/  |_||_|  V.01

        SharePoint Security Auditing by @_0rigen / 0rigen.net""")

    def brutebrowse(self):
        print("Beginning brute-force URL browsing...")
        url_requester.geturlcode(None, "test_urllist.txt")




# TODO:
# Create argument parsing to call features on-demand rather than monolithic and such

#########################################
# Command Line Arguments #
# -u URL of target
# -L file-based list of brute browsing targets
# -O specify output file rather than stdout
# ..
# ..
#########################################

parser = argparse.ArgumentParser()
parser.add_argument("-target", type=str, help="URL of the target SP site")
args = parser.parse_args()
target = args.target
if target is None:
    print("No target specified.  Use -t to specify the target URL")
    sys.exit(1)
else:

    # Set Logging level (based on command line arg in the future
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    # Ready.... FIGHT! #
    engagement = Engagement()

    print("""
        Currently Targeting: %s \n
        [B]rute Force URL Browsing for SharePoint Services (.asmx)
        [E]numeration of users
        [C]redentials Searching
        [T]arget (Change specified target URL)
        [Q]uit
        """ % target)


