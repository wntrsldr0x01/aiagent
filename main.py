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
    You are a careful AI coding agent.

Goals:
- Think step-by-step, decide if you need to use a tool, and then either call a tool or answer with plain text.
- If you need a tool, produce only a function_call with a clear name and strictly valid JSON args (no comments).
- Keep paths relative to the working directory. Do not include the working directory itself in args.
- Prefer reading and listing files before executing code. Only run code when necessary.
- After receiving a tool result, re-evaluate your plan. If more tool use is needed, call again; otherwise, return a concise final text answer.

Available tools:
- List files and directories
- Read file contents 
- Execute Python files with optional arguments 
- Write or overwrite files

Output policy:
- When youre done, respond with a clear text explanation only.
- Do not invent file names or paths. If unknown, first list or read to discover them.
- Keep function_call arguments minimal, valid, and safe.
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
            
            if response.text:
                if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
                    usage = response.usage_metadata 
                    print(f"User prompt: {user_prompt}")
                    print(f"Prompt tokens: {usage.prompt_token_count}") 
                    print(f"Response tokens:{usage.candidates_tokens_details[0].token_count}")
                    break
                print(response.text)

            for candidate in response.candidates:
                    messages.append(candidate.content)
                    for part in candidate.content.parts:
                        if part.function_call:
                            function_call_part = part.function_call 
                            print(f"Calling function: {function_call_part.name}({function_call_part.args})") #name of the function and argument passed
                            call_result = call_function(function_call_part) #actually calling the functions                                  
                            if call_result.parts[0].function_response.response:
                                mess_func_res = types.Content(role ='user', parts=[types.Part(function_response=call_result.parts[0].function_response)])
                                messages.append(mess_func_res)
                                if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
                                    print(call_result.parts[0].function_response.response)
            
                    

        except Exception as e:
            print(f"Error: {e}")