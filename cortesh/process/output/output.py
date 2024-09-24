
from abc import ABC, abstractmethod
import subprocess
import os



# Define an abstract base class (interface)
class Output(ABC):
    # Abstract method (must be implemented by any subclass)
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def get_raw(self):
        pass

    def run_command2(self, command, change_dir=None):
            # If a directory is provided, change to that directory
            if change_dir:
                os.chdir(change_dir)

            # Run the command
            result = subprocess.run(command, shell=True, capture_output=True, text=True, env=os.environ)

            # Check if the command was successful
            if result.returncode == 0:
                return result.stdout
            else:
                raise Exception(f"Command failed with error code {result.returncode} and message: {result.stderr} \n\n STDOUT: {result.stdout}")
                #return [ Error(f"Command failed with error code {result.returncode} and message: {result.stderr}") ]

    def run_command(self, command):
        try:
            # Start the process with Popen
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Communicate with the process, provide answers to the interactive prompts
            stdout, stderr = process.communicate(input='y\n')

            # Check if command succeeded
            if process.returncode == 0:
                return stdout
            else:
                raise Exception(f"Command failed with error code {process.returncode} and message: {stderr}")
        except Exception as e:
            print(f"Exception occurred: {e}")