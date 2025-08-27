from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python import run_python_file
from google.genai import types

#

TOOLS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}



def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    
    function_call_part.args['working_directory'] = './calculator'  # modifying the org args unsafe for production and hardcoded for tests
    
    function_name = function_call_part.name
    function_args = function_call_part.args

    fn = TOOLS.get(function_name)

    if not callable(fn):                                          # nudge from chatgpt to avoid uncallable entries if present
        return types.Content(
            role="tool",parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    

    function_result = fn(**function_args) # disassemble the dict according to parameter name (which is very intelligent)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result":function_result},
                )
            ],
        )


    

