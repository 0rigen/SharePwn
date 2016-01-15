from abc import ABCMeta, abstractmethod

class baseAux:
    __metaclass__ = ABCMeta

    @abstractmethod
    def scan(self): pass

    @abstractmethod
    def save(self): pass
