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

    available_functions = types.Tool(
        function_declarations = [
            schema_get_files_info,
            schema_run_python_file,
            schema_get_file_content,
            schema_write_file,
        ]
    )

    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001', 
        contents=messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction=system_prompt
            )
    )
    
    

    if response.function_calls:
        function_call_part = response.function_calls[0]    
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        call_result = call_function(function_call_part)

        if call_result.parts[0].function_response.response:
            if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
                print(call_result.parts[0].function_response.response)
        else:
            raise Exception 

    
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose" :
        usage = response.usage_metadata
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_tokens_details[0].token_count}")
    
    print(response.text)

else:
    print("please provide a prompt")
    sys.exit(1)
