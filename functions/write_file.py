import os
from .config import MAX_CHARS
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write a new file or change the content of a particular file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            )
        },
    ),
)


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        absolute_path = os.path.abspath(full_path)

        if os.path.commonpath([os.path.abspath(working_directory), absolute_path]) != os.path.abspath(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        
        with open(absolute_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
        



    except Exception as e:
        return f"Error: {e}"