
from langchain_openai import OpenAI


# A wrapper class to easily change the model and parameters of the LLM.
class LLM:
    def __init__(self, temperature=0, max_tokens=12000, model_name="gpt-4o-mini"):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model_name = model_name
        self.llm = OpenAI(temperature=self.temperature, max_tokens=self.max_tokens, model_name=self.model_name)

    def __call__(self, prompt):
        return self.invoke(prompt)

    def invoke(self, prompt):
        return self.llm.invoke(prompt)

