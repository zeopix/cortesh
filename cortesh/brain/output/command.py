from cortesh.brain.output.error import Error
from cortesh.brain.output.message import Message
from cortesh.brain.output.output import Output


class Command(Output):
    def __init__(self, command):
        self.command = command
        self.output = ''

    def process(self):
        # run the command using system call and get the output
        try:
            output = self.run_command(self.command)
            self.output = output
            return [Message(output)]
        except Exception as e:
            return [Error(str(e))]
        pass

    def render(self):
        return "Running command: " + self.command

    def get_raw(self):
        return 'COMMAND_STEP \n' + self.command + '\n\nRESULT\n' + self.output