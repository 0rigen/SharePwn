from abc_scanner import baseScanner


# Implements the baseScanner ABC by extending it
class delUser(baseScanner):
    def check(self, tgt):
        print "delUser check function was called! - scanning "+tgt.desc+" at "+tgt.ip

    def scan(self, tgt):
        print "delUser scan function was called!"

    def save(self, tgt):
        print "delUser save function was called!"
