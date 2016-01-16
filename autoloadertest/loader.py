# this will force an immediate recursive load of all modules it found - no validation yet
import tfoo
# used to read and validate detected modules
import inspect
# used to iterate through all modules
import sys

t = tfoo.framework.target.Information()
t.desc = "n00bp01nt"
t.ip = "8.8.8.8"

scnrs = []
auxes = []


# store validated modules as lists of tuples in the form of (name, class object)
# if needed for menu iteration, could store as a dictionary in the form of {name: class object}
# Iterating with tuple form: 'for n, c in list: print n+" "+c.check()'
# Iterating with dictionary form: 'for n in list.keys(): print n+" "+list[n].check()'
def clear():
    global scnrs, auxes
    scnrs = []
    auxes = []


def simpletest():
    sbase = tfoo.scanners.abc_scanner.baseScanner  # reference to the ABC
    abase = tfoo.aux.abc_aux.baseAux  # reference to the ABC
    clear()

    for s in sbase.__subclasses__():
        scnrs.append((s.__name__, s))

    for a in abase.__subclasses__():
        auxes.append((a.__name__, a))


# I apparently code things 10x as complicated as they need to be the first time around.
# The definition above is extremely smaller and makes a LOT more sense.  I'm including
# the definition of this as comments only as a point of reference in case needed elsewhere
# def loadmodules():
#     sbase = tfoo.scanners.abc_scanner.baseScanner  # reference to the ABC
#     abase = tfoo.aux.abc_aux.baseAux  # reference to the ABC
#     clear()
#
#     # iterate through all modules
#     for fqdn in sys.modules:
#         # look for known namespaces
#         if "tfoo.scanners." in fqdn:
#             # identify a list of all classes within modules
#             mc = inspect.getmembers(sys.modules[fqdn], inspect.isclass)
#
#             for c in mc:
#                 # if the class is the ABC, skip that
#                 if inspect.isabstract(c[1]):
#                     continue
#                 else:
#                     # BUT if the class is a VALID subclass of the ABC, we want to know!
#                     if issubclass(c[1], sbase):
#                         scnrs.append(c)
#
#         # repeat the process for remaining namespaces
#         if "tfoo.aux." in fqdn:
#             mc = inspect.getmembers(sys.modules[fqdn], inspect.isclass)
#
#             for c in mc:
#                 if inspect.isabstract(c[1]):
#                     continue
#                 else:
#                     if issubclass(c[1], abase):
#                         auxes.append(c)

# We could use "script name" or "metasploit-like path" to describe scripts
def getname(c, msf=False):
    if msf == True:
        return c.__module__.replace('.', '/') + "/" + c.__name__
    else:
        return c.__name__


def printlist(list, func, msf):
    for s, c in list:
        # in order to use the iterated class we need to instantiate it
        nc = c()

        # This just shows we can pull a function out by the string of its name
        f = getattr(nc, func)

        name = getname(c, msf)

        print "    - " + name + " " + func + " function results: ",
        # Execute the function we know it MUST have because it extends the ABC
        f(t)

    print ""


def execute(msf):
    print "Loaded the following scanner modules:"
    printlist(scnrs, "check", msf)
    print "Loaded the following aux modules:"
    printlist(auxes, "scan", msf)
    print "Done!"


if __name__ == "__main__":
    print "Loading all modules within the tfoo folder..."
    simpletest()

    print "Calling the \"check()\" function of all modules..."
    execute(False)

    print "Changing IP to 127.0.0.1 WITHOUT reloading modules..."
    t.ip = "127.0.0.1"

    print "Calling the \"check()\" function of all modules using MSF-style annotations..."
    execute(True)
