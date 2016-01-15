from abc import ABCMeta, abstractmethod

class baseScanner:
    __metaclass__ = ABCMeta

    @abstractmethod
    def check(self): pass

    @abstractmethod
    def scan(self): pass

    @abstractmethod
    def save(self): pass
