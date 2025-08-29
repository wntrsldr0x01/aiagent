import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


if len(sys.argv) > 1:
    user_prompt = sys.argv[1]
    system_prompt ="""
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    
    - List files and directories
    - Read file contents    
    - Execute Python files with optional arguments
    - Write or overwrite files
    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    messages = [
    types.Content(role ='user', parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(    #for every tool there should be an shcema 
        function_declarations = [
            schema_get_files_info,
            schema_run_python_file,
            schema_get_file_content,
            schema_write_file,
        ]
    )

    for i in range(0,20):         #running the agent in a loop (with an upper limit of max 20 times)
        try:
            response = client.models.generate_content(
                model = 'gemini-2.0-flash-001', 
                contents=messages,
                config = types.GenerateContentConfig(
                    tools = [available_functions],      
                    system_instruction=system_prompt
                    )
            )
            for candidate in response.candidates:
                    if candidate.content.pasts:
                        function_call_part = response.function_calls[0]    
                        print(f"Calling function: {function_call_part.name}({function_call_part.args})") #name of the function and argument passed
                        call_result = call_function(function_call_part) #actually calling the functions

                    if call_result.parts[0].function_response.response:
                        mess_func = types.Content(role ='user', parts=[types.Part(function_response=call_result.parts[0].function_response)])
                        messages.append(mess_func)

                        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
                            print(call_result.parts[0].function_response.response)
                    else:
                        raise Exception 
                    
                    messages.append(candidate.content) # I am confused between candidate and parts bc


        except Exception as e:
            print(f"Error: {e}")