"""
Create an assistant using the tools from tool_creator using the assistant creation API
"""

import os
import json
import traceback

from shared.utils import chat as chat_loop
from shared.openai_config import get_openai_client

client = get_openai_client() 

import json
import os
import traceback

def create_tool_user(assistant_details):
    try:
        print("Starting create_tool_user method")
        print(f"Assistant details received: {assistant_details}")

        # create the assistant
        print("Creating assistant...")
        tool_user = client.beta.assistants.create(**assistant_details["build_params"])
        print(f"Created assistant {tool_user.id} to use tools\n\n" + 90*"-" + "\n\n", flush=True)

        # save the assistant info to a json file
        info_to_export = {
            "assistant_id": tool_user.id,
            "assistant_details": assistant_details,
        }
        print(f"Assistant info to export: {info_to_export}")

        print("Creating directory 'assistants' if it doesn't exist...")
        os.makedirs('assistants', exist_ok=True)

        print("Writing assistant info to 'assistants/tool_user.json'...")
        with open('assistants/tool_user.json', 'w') as f:
            json.dump(info_to_export, f, indent=4)
        print("Write operation completed successfully.")

        return tool_user
    except Exception as e:
        print("An error occurred in create_tool_user method.")
        print(f"Error message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        exit(1)

def talk_to_tool_user(assistant_details):
    """
    talk to the assistant to use the tools
    """

    # check if json file exists
    try:
        os.makedirs('assistants', exist_ok=True)
        with open('assistants/tool_user.json') as f:
            create_new = input(f'Assistant details found in tool_user.json. Create a new assistant? [y/N]')
            if create_new == 'y':
                raise Exception("User wants a new assistant")
            assistant_from_json = json.load(f)
            tool_user = client.beta.assistants.retrieve(assistant_from_json['assistant_id'])
            # tool_user = client.beta.assistants.retrieve( "asst_Q0WtEKR1hjc7TkkkOXMlnj82" )
            print(f"Loaded assistant details from tool_user.json\n\n" + 90*"-" + "\n\n", flush=True)
            print(f'Assistant {tool_user.id}:\n')
            assistant_details = assistant_from_json["assistant_details"]
    except:
        # create the assistant first 
        tool_user = create_tool_user(assistant_details)

    # exec the functions from the py files
    os.makedirs('tools', exist_ok=True)
    functions = assistant_details["functions"]
    for func in functions:
        print(f"Loading function {func} into execution environment", flush=True)
        with open('tools/' + func + '.py') as f:
            exec(f.read(), globals())

        functions.update({func: eval(func)})

    # Create thread
    thread = client.beta.threads.create()

    # chat with the assistant
    chat_loop(client, thread, tool_user, functions)