from abc import ABC, abstractmethod


# Define an abstract base class (interface)
class Sense(ABC):


    @abstractmethod
    def instruction(self):
        pass

    @abstractmethod
    def test(self, response):
        pass

    @abstractmethod
    def read(self, response):
        pass