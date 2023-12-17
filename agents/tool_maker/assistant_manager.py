from agents.tool_maker.tool_manager import ToolManager
from pathlib import Path
import os
import json
from agents.agent_builder.create import AgentBuilder

class AssistantManager:

    def __init__(self, client):
        self.client = client
        self.assistant = None
        self.agent_builder = AgentBuilder(client=self.client)
        Path(__file__).absolute().parent
        tools_path = os.path.join(
            Path(__file__).absolute().parent, "tool_creator_metadata.json"
        )
        with open(tools_path, "r") as file:
            self.assistant_package = json.load(file)

    def get_assistant(self):
        """Retrieve or create an assistant for testing this functionality"""
        name = self.assistant_package["creator"]["name"]
        self.agent_builder.create_assistant(name)
        if not name in [
            assistant.name for assistant in self.client.beta.assistants.list()
        ]:
            raise ValueError(f'{name} needs to be created using create.py in /agents/agent_builder/')
        else:
            assistant_dict = {
                assistant.name: assistant.id
                for assistant in self.client.beta.assistants.list()
            }
            assistant = self.client.beta.assistants.retrieve(
                assistant_id=assistant_dict[name]
            )
        self.assistant = assistant
        return assistant

    def get_coding_assistant(self):
        """Retrieve or create an assistant for testing this functionality"""
        name = self.assistant_package["writer"]["name"]
        self.agent_builder.create_assistant(name)
        if not name in [
            assistant.name for assistant in self.client.beta.assistants.list()
        ]:
            raise ValueError(f'{name} needs to be created using create.py in /agents/agent_builder/')
        else:
            assistant_dict = {
                assistant.name: assistant.id
                for assistant in self.client.beta.assistants.list()
            }
            assistant = self.client.beta.assistants.retrieve(
                assistant_id=assistant_dict[name]
            )
        self.assistant = assistant
        return assistant

    def make_tool_creation_assistant(self):
        tools = [
            ToolManager.tool_from_function_schema(
                json.loads(AssistantManager.request_function_tool)
            )
        ]
        assistant = self.client.beta.assistants.create(
            model=self.assistant_package["model"],
            description=self.assistant_package["description"],
            instructions=self.assistant_package["instructions"],
            name=self.assistant_package["name"],
            tools=tools,
        )
        return assistant

    def make_coding_assistant(self):
        code_assistant = self.client.beta.assistants.create(
            model="gpt-3.5-turbo-1106",
            instructions="you will be provided a json schema of an OpenAI function tool from an API not a human user. The json will contain all information about the function you will need to write it in python code. You will return only the python function you wrote and no additional text as you are talking to an API and extraneous output will cause execution errors. You must always implement the actual code. Generic placeholders or pseudo code will break the api. If you need clarification to write real functioning code, request for extra info in arguments without creating a real function or valid schema",
            name="temporary_function_writer",
        )
        return code_assistant


if __name__ == "__main__":
    from  shared.openai_config import get_openai_client

    client = get_openai_client()

    assistant_manager = AssistantManager(client=client)
    assistant = assistant_manager.get_assistant()
    print(assistant)
