import logging

""" Printer takes an output intended for the console and colors it
as well as adds an appropriate icon.  Printer also is called to
display the SharePwn banner and the Engagement Menu.

Legend:
[?] - Need input form user
[!] - Error or Failure
[*] - Status/Success
[...] - Working
"""


class Printer:
    # Colors for terminal output
    red = "\033[31m"  # errors
    cyan = "\033[36m"  # menu items
    yellow = "\033[33m"  # information and requests
    green = "\033[92m"  # Information and success
    blue = "\033[94m"  # other
    endc = "\033[0m"  # end the current color
    bold = "\033[1m"
    underline = "\033[4m"

    def __init__(self):
        logging.debug("Printer object initialized.")

    # Print string in yellow with [?] prepended, Returns the inputted string
    def input(self, in_string):
        in_string = str(in_string)  # just to be safe
        in_string = self.yellow + "[?] " + in_string + self.endc
        var = raw_input(in_string)
        return var

    # Print string in red with [!] prepended
    def error(self, in_string):
        in_string = str(in_string)  # just to be safe
        in_string = self.red + "[!] " + in_string + self.endc
        print in_string

    # Print string in green with [*] prepended
    def status(self, in_string):
        in_string = str(in_string)  # just to be safe
        in_string = self.green + "[*] " + in_string + self.endc
        print in_string

    # Print string in blue with [...] prepended
    def working(self, in_string):
        in_string = str(in_string)  # just to be safe
        in_string = self.blue + "[...] " + in_string + self.endc
        print in_string

    # Print string in cyan
    def menu(self, in_string):
        in_string = str(in_string)  # just to be safe
        in_string = self.cyan + in_string + self.endc
        print in_string

    # Show the SharePwn banner after clearing the screen
    def banner(self):
        """ banner clears the console and displays the SharePwn banner
        This should be called when a new engagement is created
        :return:
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[95m" + self.bold + """
          ___   _                         ___
         / __| | |_    __ _   _ _   ___  | _ \ __ __ __  _ _
         \__ \ | ' \  / _` | | '_| / -_) |  _/ \ V  V / | ' \\
         |___/ |_||_| \__,_| |_|   \___| |_|    \_/\_/  |_||_|  BETA

        SharePoint Security Auditing by @_0rigen / 0rigen.net""" + self.endc)

    def show_menu(self):
        """ showmenu - display the Engagement menu on the console

        :return: char, menu choice
        """
        while True:
            print(self.cyan + self.underline + "Please choose an option below: \n" + self.endc)
            print("[" + self.yellow + "B" + self.endc + self.cyan + "]rute Force Browsing")
            print("[" + self.yellow + "V" + self.endc + self.cyan + "]ersion Information")
            # print("[" + yellow + "S" + endc + cyan + "]ervice Interrogater")
            print("[" + self.yellow + "P" + self.endc + self.cyan + "]eople Service Enumeration")
            print("[" + self.yellow + "U" + self.endc + self.cyan + "]serID Brute Force Search")
            print("[" + self.yellow + "A" + self.endc + self.cyan + "]uthentication Configuration")
            print("[" + self.yellow + "T" + self.endc + self.cyan + "]arget (Change your target URL/Protocol)")
            print("[" + self.yellow + "O" + self.endc + self.cyan + "]utput Redirection (Print to a file)")
            print("[" + self.yellow + "Q" + self.endc + self.cyan + "]uit and go home")
            choice = raw_input("Command: " + self.endc)
            if choice.capitalize() == 'B':
                return 'B'
            elif choice.capitalize() == 'V':
                return 'V'
            # elif choice.capitalize() == 'S':
            #    service_interrogator.submenu(tar)
            elif choice.capitalize() == 'P':
                return 'P'
            elif choice.capitalize() == 'U':
                return 'U'
            elif choice.capitalize() == 'A':
                return 'A'
            elif choice.capitalize() == 'T':
                return 'T'
            elif choice.capitalize() == 'O':
                return 'O'
            elif choice.capitalize() == 'Q':
                return 'Q'
            else:
                self.error("Command not understood; try again, buddy!")
