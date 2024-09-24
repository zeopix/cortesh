from cortesh.process.output.error import Error
from cortesh.process.output.output import Output
import os

class CreateFile(Output):
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def process(self):
        # create file
        try:
            #create directory if it doesn't exist

            os.makedirs(os.path.dirname(self.name), exist_ok=True)
            #if the file exists, empty it first
            with open(self.name, 'w') as f:
                f.write(self.content)
        except Exception as e:
            return [Error(str(e))]
        return []

    def render(self):
        return "Creating file: " + self.name

    def get_raw(self):
        return 'FILE_STEP \n' + self.name + '\n\nFILE_NAME_SEPARATOR\n' + self.content