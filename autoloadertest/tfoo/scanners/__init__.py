# Modified from from http://www.stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python
# Used to programatically import files from directory
import pkgutil

# Extend the default importer's search path to include the current directory (name of package)
__path__ = pkgutil.extend_path(__path__, __name__)

# walk_packages() will pull out information for detected modules and prefix it with current
# package name so FQDN will be "tfoo.scanners.<modulename>"
for impt, name, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__ + '.'):
    __import__(name)
