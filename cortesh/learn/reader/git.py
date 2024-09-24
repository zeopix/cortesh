import os

from langchain_core.prompts import PromptTemplate


class GitReader():
    prompt_template = """
    Summarize the file {path}.
    
    Blamed file content and commit descriptions:
    {annotations}
    
    Raw file Content
    {content}
    """
    def __init__(self, llm):
        self.llm = llm

    def read(self, path):
        # Annotate the current file.
        # Prepare a prompt to make a summary of the entire file, containing every commit name above the changes made in the file.
        file = open(path, 'r')
        # obtain annotations from git command
        annotations = self.get_annotations(path)
        prompt = self.prompt_template.format(path=path, content=file.read(), annotations=annotations)
        self.llm.invoke(prompt)

    def get_annotations(self, path):
        command = 'git blame --date=format: ' + path
        blame_output = os.popen(command).read()
        # now use git log to get the commit names
        commit_hashes = self.get_commit_hashes(blame_output)
        commit_names = self.get_commit_names(commit_hashes)

        return '\n'.join(commit_names) +  '\n' + path + '\n' + blame_output

    def get_commit_hashes(self, blame_output):
        commit_names = []
        for line in blame_output.split('\n'):
            if line != '':
                commit = line.split(' ')[0]
                commit_names.append(commit)
        return commit_names

    def get_commit_names(self, commit_hashes):
        commit_names = []
        for commit in commit_hashes:
            command = 'git log -1 --pretty=format:"%s" ' + commit
            commit_name = os.popen(command).read()
            commit_names.append(commit_name)
        return commit_names