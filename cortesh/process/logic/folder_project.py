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


class FolderProject(Logic):
    actions = [
        FolderStructure(),
        FileContent(),
        CommandResponse()
    ]
    template = """
The user has requested the following: {prompt}

Please provide the structured information step by step. 
Do not include markdown other than the three ``` or any other unneccessary information, do not provide list prefixes or numbering, do not include colons or any other punctuation in the headings.
The workspace is the current directory, do not create a new directory for the project. Make sure the project is created in the current directory.
All the commands must be non-interactive.

If more information is needed about the folder structure, or the content of some specific files, 
to clarify how they need to be integrated or updated for the user request, just return, one of the following commands:
{actions}

Please, make sure you have all the file content information before updating or creating new files. 
Do not ask the same action on the same file more than once. Do not try to ask for files or folders that do not exist, 
just create the necessary ones in the response.

If you need to update one file, please add it as a new file, and provide the content that should be in the file, avoid using ``sed`` and similar commands.
Provide the full path for creating files and do not use ``cd`` command to change the directory.

If no more information is needed, then the response will start with
=== RESPONSE ===

Later, each step should be in the following format:
- For a command, use 'COMMAND_STEP', for example:
   COMMAND_STEP
   ```
   <command>
   ```

- For a file creation, use 'FILE_STEP', 'FILENAME_SEPARATOR', and 'CONTENT_SEPARATOR', for example:
   FILE_STEP
   ```
   <filename>
   ```
   FILENAME_SEPARATOR
   ```
   <file content>
   ```

The steps should be provided in the exact order they should be executed. Ensure each step is complete before proceeding to the next.

{actions_info}
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
            parsed_data = self.parse_response(response.content)
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
            Is the following user request, asking to create a new project, or update a feature in a existing one, that can be achieved trough running command lines and creating source files? Please print the output as true or false.
            {prompt}
            """
        )
        #chain = LLMChain(llm.py=self.llm.py, prompt=template)
        #response = chain.run(prompt=prompt)
        final_prompt = template.format(prompt=prompt)
        self.logger.log('- Prompt')
        self.logger.log(final_prompt)
        response = self.llm(final_prompt)
        self.logger.log('- Response')

        result = False
        try:
            # cast to boolean
            result = response.content.strip().lower() == 'true'
        except json.JSONDecodeError:
            # maybe log something
            return None
        return result

    def process(self, prompt, actions_info='', depth=0):

        promptTemplate = PromptTemplate(
            input_variables=["prompt", "actions", "actions_info"],
            template=self.template
        )

        final_prompt = promptTemplate.format(prompt=prompt, actions=self.get_prompt_actions(), actions_info=actions_info)
        response = self.logged_llm(final_prompt)

        try:
            extra_info = self.parse_actions(actions_info, response.content)

            if extra_info and depth < 40:
                return self.process(prompt, extra_info, depth+1)
            parsed_data = self.parse_response(response.content)
        except Exception as e:
            print(e)
            return [Message("Sorry, I cannot create this project.")]

        return [
            Message("Creating a new project..."),
            *parsed_data
        ]

    def logged_llm(self, final_prompt):
        # Get the structured output from the LLM
        self.logger.log('- Prompt')
        self.logger.log(final_prompt)
        response = self.llm(final_prompt)
        self.logger.log('- Response')
        self.logger.log(response.content)
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
        # Check if response contains === REQUEST_FOLDER_STRUCTURE:<foldername> ===

        # Extract commands and files based on steps

        # todo, this needs to be imported from eac output class. This is a temporary solution
        #steps = re.findall(r'(COMMAND_STEP\n(.*?)\n|FILE_STEP\n(.*?)\nFILENAME_SEPARATOR\n(.*?)\n)', response,
        #                   re.DOTALL)
        steps = re.findall(r'(COMMAND_STEP\n```\n(.*?)\n```|FILE_STEP\n```\n(.*?)\n```\nFILENAME_SEPARATOR\n```\n(.*?)\n```)', response,
                           re.DOTALL)

        parsed_steps = []

        for step in steps:
            if step[1]:  # If it's a command
                parsed_steps.append( Command(step[1].strip() ) )
            elif step[2]:  # If it's a file creation
                parsed_steps.append( CreateFile( step[2].strip(), step[3].strip() ) )

        return parsed_steps


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


