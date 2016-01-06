class Authentication:
    # Constants
    '''
    Could contain all session establishment handling here...
    Depending on which type of auth is called, we can establish the appropriate session within
       that same function definition...
    '''
    type = None  # cookie, ntlm, or None
    user = None
    paswd = None
    cookie = None

    # Function definitions
    def __init__(self):
        self.data = []


########################
"""
Old copy-pasted stuff that needs to find a home here
"""


###################################################
# Configures either NTLM or Cookie authentication #
# ntlm - return a couplet of username:password    #
# cookie - return a cookie jar                    #
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
        # TODO This isn't workin yet.
        elif type.capitalize().startswith("C"):
            lwp_cj = cookielib.LWPCookieJar()
            cookie_file = raw_input(blue + "Cookie File Location: " + endc)
            print(yellow + "[*]" + endc + " Loading cookie from %s" % str(cookie_file))
            cookie_file = str(cookie_file)
            try:
                lwp_cj.load(cookie_file, ignore_discard=True, ignore_expires=True)
                print(green + "[*]" + endc + " Cookies loaded into CookieJar, We're ready to go!")
                req_cj = requests.utils.dict_from_cookiejar(lwp_cj)
                print str(reqs_cj)
                return reqs_cj
            except:
                print(red + "[!] " + endc + "Failed to load cookie.")
                break
                # session = requests.session(cookies=cookies)
                # The above line needs to go into the request location
