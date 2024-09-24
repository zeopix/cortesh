from socket import send_fds

from cortesh.brain.logic.folder_project import FolderProject
from cortesh.brain.output.message import Message


class Learn:
    def __init__(self, llm, logger):
        self.llm = llm
        self.logger = logger

    def input(self, prompt):

