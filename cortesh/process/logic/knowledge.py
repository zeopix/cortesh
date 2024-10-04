from langchain_core.prompts import PromptTemplate

from cortesh.process.logic.base import Logic
from cortesh.process.output.command import Command
from cortesh.process.output.create_file import CreateFile
from cortesh.process.output.message import Message
import json
import re

from cortesh.process.sense.command_response import CommandResponse
from cortesh.process.sense.file_content import FileContent
from cortesh.process.sense.folder_structure import FolderStructure
from cortesh.process.memory.memory import Memory


class Knowledge(Logic):
    actions = [
        FolderStructure(),
        FileContent(),
        CommandResponse()
    ]
    templateSystem = """
Prepare a text query, optimized for querying the embeddings database, to search for the requested information in the project memory.
Given the following user request: 
"""
    template = """
    {prompt}
        """


    def process_fix(self, prompt, previous_outputs):
        templateWithOutput= self.template + "\n\n" + "The user is trying the following steps and the output is not as expected. Please provide the correct steps.\n\n{steps}"


        output_results = "\n\n".join([output.get_raw() for output in previous_outputs])

        promptTemplate = PromptTemplate(
            input_variables=["prompt","steps", "actions"],
            template=templateWithOutput
        )

        final_prompt = promptTemplate.format(prompt=prompt, steps=output_results, actions=self.get_prompt_actions())
        response = self.logged_llm(final_prompt)

        try:
            parsed_data = self.parse_response(response)
        except Exception as e:
            print(e)
            return [Message("Sorry, I cannot create this project.")]

        return [
            Message("Creating a new project..."),
            *parsed_data
        ]

        pass

    def test(self, prompt):
        return True
        template = PromptTemplate(
            input_variables=["prompt"],
            template="""
            Is the following user request, asking to just a question about the current project, without requesting any change, perform any update, nor add or remove dependencies.
            {prompt}
            """
        )
        #chain = LLMChain(llm.py=self.llm.py, prompt=template)
        #response = chain.run(prompt=prompt)
        final_prompt = template.format(prompt=prompt)
        self.logger.log('- Prompt')
        self.logger.log(final_prompt)
        response = self.llm.invoke(final_prompt)
        self.logger.log('- Response')

        result = False
        try:
            # cast to boolean
            result = response.strip().lower() == 'true'
        except json.JSONDecodeError:
            # maybe log something
            return None
        return result

    def process(self, prompt, actions_info='', depth=0):


        memory = Memory('git')
        print('Ask:', prompt)
        
        prompt = self.llm.invoke(self.templateSystem + "\n" + prompt + "\n **Query for Embeddings Database:**")

        print('Search in embeddings: ', prompt)
        memoryEntries = memory.find(prompt)

        filteredMemoryEntries = []
        
        for entry in memoryEntries:
            metadata = entry.metadata
            page_content = entry.page_content
            if 'key' in metadata:
                entryText = 'Memory entry file: \n' + metadata['key'] + "\n\n Memory entry description: \n" + page_content + '\n\n -------- \n\n'
                print(' - Memory entry key:', metadata['key'])
                # open file
                content = open(metadata['key'], 'r').read()
                entryText = entryText + 'File content: \n' + content + '\n\n -------- \n\n'
                filteredMemoryEntries.append(entryText)
        
        postprompt = (
            "The user has requested the following: " + prompt + "\n\n"
            "Knowing that there is a database of embeddings containing summaries of each file of the project. \n"
            "The embeddings are generated with filenames as keys and the embedding value is obtained from a summary\n"
            "of the file content, together with the involved commit description, making it possible to index the specific\n"
            "meaning of that file in the context of the project.\n\n"
            "Knowing this, and the result of the search query, elaborate response that will be used to answer the user prompt, knowing it's a answer for the specific project memory.\n\n"
        )

        if len(filteredMemoryEntries) > 0:
            postprompt = postprompt + "The following files were found in the project with the requested information:\n\n" + "".join(filteredMemoryEntries)
        else:
            postprompt = postprompt + "No files were found in the project with the requested information. Return a message to inform the user.\n\n"

        postresponse = self.llm.invoke(postprompt)

        return [Message(postresponse)]
        promptTemplate = PromptTemplate(
            input_variables=["prompt"],
            template=self.template
        )

        final_prompt = promptTemplate.format(prompt=prompt)
        response = self.logged_llm(final_prompt)

        try:
            extra_info = self.parse_actions(actions_info, response)

            if extra_info and depth < 40:
                return self.process(prompt, extra_info, depth+1)
            parsed_data = self.parse_response(response)
        except Exception as e:
            print(e)
            return [Message("Sorry, I cannot create this project.")]

        return [
            Message("Searching in knowledge..."),
            *parsed_data
        ]

    def logged_llm(self, final_prompt):
        # Get the structured output from the LLM
        self.logger.log('- Prompt')
        self.logger.log(final_prompt)
        response = self.llm(final_prompt)
        self.logger.log('- Response')
        self.logger.log(response)
        return response

    def parse_actions(self, actions_info, response):
        hadActions = False
        for action in self.actions:
            if action.test(response):
                hadActions = True
                if actions_info == '':
                    actions_info = 'This the information requested in previous prompts:'
                actions_info = actions_info + '\n' + action.read(response)
        return actions_info if hadActions else False

    def parse_response(self, response):
        return [ Message(response) ]


    def validate(self, prompt):



        # Write a test to validate the output
        # Run the test and collect output.

        # Check if the test was successful
        # If not, check the commands output.
        # If nothing there, check the test output
        # If still nothing, return False
        return True

    def get_prompt_actions(self):
        return "\n".join([action.instruction() for action in self.actions])


