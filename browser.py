__author__ = 'Origen'

import requests

###############################################
##          Request Pages                    ##
# page - single url to request                 #
# bdict - file containing brute dictionary     #
###############################################
def request(page = None, bdict = None):
    if(bdict is not None):
        print("Beginning dictionary-based brute force browse...")
    elif(page is not None):
        print ("Requesting %s" % page)
        try:
            resp = requests.get(page)
            #returned_code = response.getcode()
            #print returned_code
        except:
            print("bad")

    else:
        print("Something went very, very wrong.")
        sys.exit(1)

def parse(code):
    print("Parsing codes!")

def disp():
    print("Display output?")