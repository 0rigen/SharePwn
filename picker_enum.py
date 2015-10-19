import requests
import url_processor

__author__ = '0rigen'
__email__ = "0rigen@0rigen.net"
__status__ = "Prototype"


###############################################
# Uses the picker.aspx service to enumerate
# users, systems, and other accounts.
##############################################

def picker_enum(target):
    target = url_processor.checkhttp(target)
    target = target + "/_layouts/Picker.aspx"

    # Build Request