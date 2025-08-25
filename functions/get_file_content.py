import os
from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        absolute_path = os.path.abspath(full_path)

        if os.path.commonpath([os.path.abspath(working_directory), absolute_path]) != os.path.abspath(working_directory):  #creating the boundry condition where the user cannot escape the working dir
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        if not os.path.isfile(absolute_path): #check if file exists
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(absolute_path, "r") as f:
            file_content_string = f.read(MAX_CHARS+1) #check if the file actually has more than max chars or not

            if len(file_content_string) > MAX_CHARS:
                truncated = file_content_string[:MAX_CHARS] + f' [...File "{file_path}" truncated at {MAX_CHARS} characters]' #read only max chars
                return truncated
            else:
                return file_content_string[:MAX_CHARS] 
            
    except Exception as e:
        return f"Error: {e}"