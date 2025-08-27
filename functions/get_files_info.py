import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        absolute_path = os.path.abspath(full_path)

        if os.path.commonpath([os.path.abspath(working_directory), absolute_path]) != os.path.abspath(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(absolute_path):
            return f'Error: "{directory}" is not a directory'
        
        files = os.listdir(path=absolute_path)
        file_metadata = []

        for file in files:
            mdata = f"- {file}: file_size={os.path.getsize(os.path.join(absolute_path, file))} bytes, is_dir={os.path.isdir(os.path.join(absolute_path, file))}"
            file_metadata.append(mdata)
        
        return "\n".join(file_metadata)
            
        



    except Exception as e:
        return f"Error: {e}"
        
    

    

    
