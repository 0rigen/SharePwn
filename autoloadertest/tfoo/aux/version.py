from abc_aux import baseAux

# This file contains TWO VALID classes.  Both show up individually, with a shared FQDN namespace
# ... allows for organization / consolidation?

class iis(baseAux):
    def scan(self, tgt):
        print "This would return the version of IIS running on " + tgt.desc + " at " + tgt.ip

    def save(self):
        print "iis save function was called!"


class sharepoint(baseAux):
    def scan(self, tgt):
        print "This would return the version of Sharepoint running on " + tgt.desc + " at " + tgt.ip

    def save(self):
        print "sharepoint save function was called!"
