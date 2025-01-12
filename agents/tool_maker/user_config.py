import json
import os

import os
import json

class AssistantConfig:
    def __init__(self, tools_to_use=None):
        print("Initializing AssistantConfig...")
        self.tools_to_use = tools_to_use or []
        print(f"Tools to use: {self.tools_to_use}")
        self.instructions_for_assistant = 'Use the tools to accomplish the task'
        self.files_for_assistant = []  # Local file paths
        self.assistant_details = self._build_assistant_details()
        print("Initialization complete.")

    def _build_assistant_details(self):
        print("Building assistant details...")
        assistant_details = {
            'build_params': {
                'model': "gpt-3.5-turbo-1106",
                'name': "Tool User",
                'description': "Assistant to use tools made by the tool creator.",
                'instructions': self.instructions_for_assistant,
                'tools': [],  # Tools will be added in the loop below
                'file_ids': [],
                'metadata': {},
            },
            'file_paths': self.files_for_assistant,
            'functions': {},  # Functions will be added in the loop below
        }

        # Load tools and their details
        os.makedirs('tools', exist_ok=True)
        if not self.tools_to_use:
            self.tools_to_use = [tool.split('.')[0] for tool in os.listdir('tools') if tool.endswith('.py')]
        print(f"Tools after loading: {self.tools_to_use}")

        for tool in self.tools_to_use:
            print(f"Processing tool: {tool}")
            with open(f'tools/{tool}.json') as f:
                tool_details = json.load(f)
            print(f"Loaded tool details: {tool_details}")

            with open(f'tools/{tool}.py') as f:
                tool_code = f.read()
            print(f"Read tool code for {tool}")

            assistant_details['build_params']['tools'].append({
                "type": "function",
                "function": {
                    "name": tool_details['name'],
                    "description": tool_details['description'],
                    "parameters": tool_details['parameters'],  # Directly use the dictionary
                },
            })
            assistant_details['functions'][tool_details['name']] = tool_code

        print("Assistant details built successfully.")
        return assistant_details

