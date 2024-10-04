from cortesh.process.sense.sense import Sense
import subprocess

class CommandResponse(Sense):
    def instruction(self):
        return '=== REQUEST_COMMAND:<command> === - for example a command to run tests and check the failing one. Should not be used to make changes, only to read project status somehow.'

    def test(self, response):
        if '=== REQUEST_COMMAND:' in response:
            return True
        pass

    def read(self, response):
        requested_folder_structures = []
        for line in response.split('\n'):
            if '=== REQUEST_COMMAND:' in line:
                command = line.split('=== REQUEST_COMMAND:')[1].strip().split('===')[0]
                print('---RUNNING COMMAND: ' + command)
                requested_folder_structures.append( self.run_command(command))


        return '\n'.join(requested_folder_structures)

    def run_command(self, command):
        # Start the process with Popen
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

        # Communicate with the process, provide answers to the interactive prompts
        stdout, stderr = process.communicate(input='y\n')

        # Check if command succeeded
        if process.returncode == 0:
            return stdout
        else:
            raise Exception(f"Command failed with error code {process.returncode} and message: {stderr}")
        # return all in text format

        return '=== REQUEST_COMMAND:' + command + ' ===\n\n' + content