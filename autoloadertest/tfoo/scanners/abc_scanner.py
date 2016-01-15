from abc import ABCMeta, abstractmethod

class baseScanner:
    __metaclass__ = ABCMeta

    @abstractmethod
    def check(self, tgt): pass

    @abstractmethod
    def scan(self, tgt): pass

    @abstractmethod
    def save(self, tgt): pass
