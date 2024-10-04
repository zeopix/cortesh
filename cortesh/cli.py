import os
from dotenv import load_dotenv, set_key
from langchain_openai import ChatOpenAI
from cortesh.interface.llm import LLM
from cortesh.config import Config
from cortesh.learn.learn import Learn
from cortesh.process.process import Process
from cortesh.interface.logger import Logger


def setup_api_key():
    """Check for OpenAI API key in .env file or prompt the user to enter it."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        api_key = input("Please enter your OpenAI API key: ")
        # Save the API key to .env file
        set_key('.env', 'OPENAI_API_KEY', api_key)


def initialize_langchain():
    """Initialize the LangChain LLM with OpenAI."""
    llm = ChatOpenAI(temperature=0, max_tokens = 12000, model_name = "gpt-4o-mini")
    return llm


setup_api_key()
llm = LLM()

def main():
    # check if any arg is present, if '--index' is present, index the folders and extensions
    import sys
    for arg in sys.argv:
        if arg == '--index':
            index()
            return
    print("Welcome to cortesh! Your AI pair programmer.")
    print("Enter your requests (type 'exit' to quit):")
    process = Process(llm, Logger())
    while True:
        user_request = input("> ")
        if user_request.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        outputs = process.input(user_request)


def index():
    #Check if there is a .cortesh folder, if not create it
    if not os.path.exists('.cortesh'):
        os.mkdir('.cortesh')
    #check if there is an existing index.toml file, if so, ask if they want to overwrite it
    
    newllm = LLM()
    config = Config()
    learn = Learn(newllm, Logger(), config)
    learn.index()


def explore():
    if not os.path.exists('.cortesh'):
        os.mkdir('.cortesh')
    #check if there is an existing index.toml file, if so, ask if they want to overwrite it
    newllm = LLM()
    config = Config()
    learn = Learn(newllm, Logger(), config)
    learn.explore()