import people_enum
import requests
import sharepwn

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


######################
# Picker Enumeration #
######################
def peopleenumeration(target, creds):
    people_enum.search(target, creds)


###################################
# Show the menu                   #
# @tar - the target, port couplet #
###################################
def submenu(tar):
    while True:
        print(endc + blue + "\n[*] Targeting: %s:%s [*]" % (tar[0], tar[1]) + endc)
        if auth is None:
            print(endc + blue + "[*] Testing as an Unauthenticated user" + endc)
        elif type(auth) is str:
            print(endc + blue + "[*] Using Cookie Saved At: %s [*]" % auth + endc)
        elif type(auth) is list:
            print(endc + blue + "[*] Authenticating as " + green + "%s:%s" + endc) % (str(auth[0]), str(auth[1]))
        print(cyan + "Please choose a service to interrogate: \n")
        print("[" + yellow + "P" + endc + cyan + "]eople Service Enumeration")
        print("[" + yellow + "U" + endc + cyan + "]serID Brute Force Search")
        # Future service interrogation modules get added to this menu
        print("[" + yellow + "B" + endc + cyan + "]ack")
        choice = raw_input("Service: " + endc)
        if choice.capitalize() == 'P':
            peopleenumeration(tar, auth_type)
        elif choice.capitalize() == 'U':
            useridenumeration(tar)
        elif choice.capitalize() == 'B':
            sharepwn.showmenu(tar)
        else:
            print(yellow + bold + "[!] Command not understood; try again, buddy!" + endc)
