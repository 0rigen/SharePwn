# this will force an immediate recursive load of all modules it found - no validation yet
import tfoo
# used to read and validate detected modules
import inspect
# used to iterate through all modules
import sys

# store validated modules as lists of tuples in the form of (name, class object)
scnrs = []
auxes = []
t = tfoo.framework.target.Information()
t.desc = "n00bp01nt"
t.ip = "8.8.8.8"


def loadmodules():
    sbase = tfoo.scanners.abc_scanner.baseScanner  # reference to the ABC
    abase = tfoo.aux.abc_aux.baseAux  # reference to the ABC

    # iterate through all modules
    for fqdn in sys.modules:
        # look for known namespaces
        if "tfoo.scanners." in fqdn:
            # identify a list of all classes within modules
            mc = inspect.getmembers(sys.modules[fqdn], inspect.isclass)

            for c in mc:
                # if the class is the ABC, skip that
                if inspect.isabstract(c[1]):
                    continue
                else:
                    # BUT if the class is a VALID subclass of the ABC, we want to know!
                    if issubclass(c[1], sbase):
                        scnrs.append(c)

        # repeat the process for remaining namespaces
        if "tfoo.aux." in fqdn:
            mc = inspect.getmembers(sys.modules[fqdn], inspect.isclass)

            for c in mc:
                if inspect.isabstract(c[1]):
                    continue
                else:
                    if issubclass(c[1], abase):
                        auxes.append(c)

    print "Loaded the following scanners:"
    for s, c in scnrs:
        # in order to use the iterated class we need to instantiate it
        nc = c()
        print "    - " + s + " check function results: ",
        # Execute the function we know it MUST have because it extends the ABC
        nc.check(t)

    print ""

    # Repeat for remaining namespaces
    print "Loaded the following aux modules:"
    for a, c in auxes:
        nc = c()
        print "    - " + a + " scan function results: ",
        nc.scan()

    print ""
    print "Done!"


# Call the function we just defined so it displays something
loadmodules()
