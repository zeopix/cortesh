import os
from dotenv import load_dotenv, set_key
from langchain_openai import ChatOpenAI

from cortesh.brain.process import Process
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
llm = initialize_langchain()

def main():
    print("Welcome to cortesh! Your AI pair programmer.")
    print("Enter your requests (type 'exit' to quit):")
    process = Process(llm, Logger())
    while True:
        user_request = input("> ")
        if user_request.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        outputs = process.input(user_request)
