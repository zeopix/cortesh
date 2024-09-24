from socket import send_fds

from cortesh.process.logic.folder_project import FolderProject
from cortesh.process.output.message import Message


class Process:
    def __init__(self, llm, logger):
        self.llm = llm
        self.identification = None
        self.tasksResults = []
        self.logger = logger

    def input(self, prompt):
        classes = [
            FolderProject(self.llm, self.logger),
        ]

        r = [Message("I'm sorry, I don't understand that request.")]

        for c in classes:
            if c.test(prompt):
                r = c.process(prompt)
                self.identification = c
                break

        self.try_and_retry_tasks(prompt, r)
        self.identification = None

    def try_and_retry_tasks(self, prompt, tasks, depth=0):
        if tasks and len(tasks) > 0:
            try:
                self.tasksResults = []
                self.process_tasks(tasks)
            except Exception as e:
                print(e)
                if depth > 3:
                    return
                depth += 1
                new_tasks = self.identification.process_fix(prompt, self.tasksResults )
                self.try_and_retry_tasks( prompt, new_tasks, depth)

    def process_tasks(self, tasks):
        for task in tasks:
            self.tasksResults.append(task)
            # check if task is type Error
            if task.__class__.__name__ == 'Error':
                print('-----error found')
                print(task.render())
                raise Exception(task.render())
                break
            print(task.render())
            output_tasks = task.process()

            if output_tasks and len(output_tasks) > 0:
                self.process_tasks(output_tasks)


