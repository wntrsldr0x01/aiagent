import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run any Python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to run files from, relative to the working directory. If not provided, run files in the working directory itself.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        absolute_path = os.path.abspath(full_path)

        if os.path.commonpath([os.path.abspath(working_directory), absolute_path]) != os.path.abspath(working_directory):  #creating the boundry condition where the user cannot escape the working dir
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(absolute_path): #check if file exists
            return f'Error: File "{file_path}" not found.'
        
        root, ext = os.path.splitext(absolute_path)

        if ext != ".py":  #extension checker
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            command = ["python3", absolute_path] + args
            completed_process = subprocess.run(command, cwd=working_directory ,check=False, capture_output=True, text=True , timeout=30) #Runs the subprocess with 30 seconds as limit and text=true so the output stream is not it bytes cwd is set just in case
            
            # I struggled with the bit below this comment basically checking the conditions and preparing an output
            cresult = completed_process.stdout   
            cerror = completed_process.stderr
            
            output_lines = [f"STDOUT:{cresult}", f"STDERR:{cerror}"]
            
            if not cresult.strip() and not cerror.strip():
                return f"No output produced"
            
            if completed_process.returncode != 0:
                output_lines.append(f"Process exited with code {completed_process.returncode}")
                fresults = "\n".join(output_lines)
                return fresults

            else:
                fresults = "\n".join(output_lines)
                return fresults
        
        except Exception as e:
            return f"Error: executing Python file: {e}"

    
    except Exception as e:
        return f"Error: {e}"
