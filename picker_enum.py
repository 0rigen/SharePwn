import requests
import url_processor

__author__ = '0rigen'


###############################################
# Uses the picker.aspx service to enumerate
# users, systems, and other accounts.
##############################################

def picker_enum(target):
    target = url_processor.checkhttp(target)
    target = target + "/_layouts/Picker.aspx"

    # Build Request