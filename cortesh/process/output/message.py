from cortesh.brain.output.output import Output


class Message(Output):
    def __init__(self, message):
        self.message = message

    def process(self):
        pass

    def render(self):
        return self.message

    def get_raw(self):
        return ''