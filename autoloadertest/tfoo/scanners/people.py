from abc_scanner import baseScanner

# This file contains TWO VALID classes.  Both show up individually, with a shared FQDN namespace
# ... allows for organization / consolidation?

class enumUsers(baseScanner):
    def check(self, tgt):
        print "check function was called!"

    def scan(self, tgt):
        print "enumUsers scan function was called!"

    def save(self, tgt):
        print "enumUsers save function was called!"


class addUsers(baseScanner):
    def check(self, tgt):
        print "addUsers check function was called!"

    def scan(self, tgt):
        print "addUsers scan function was called!"

    def save(self, tgt):
        print "addUsers save function was called!"
