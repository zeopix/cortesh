from abc import ABC, abstractmethod


# Define an abstract base class (interface)
class Logic(ABC):
    def __init__(self, llm, logger):
        self.llm  = llm
        self.logger = logger
    # Abstract method (must be implemented by any subclass)
    @abstractmethod
    def test(self, prompt):
        pass

    # Another abstract method
    @abstractmethod
    def process(self, prompt):
        pass

    @abstractmethod
    def validate(self, prompt):
        pass

    # Another abstract method
    @abstractmethod
    def process_fix(self, prompt, output_results):
        pass