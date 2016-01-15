from abc_scanner import baseScanner


# Implements the baseScanner ABC by extending it
class delUser(baseScanner):
    def check(self):
        print "delUser check function was called!"

    def scan(self):
        print "delUser scan function was called!"

    def save(self):
        print "delUser save function was called!"
