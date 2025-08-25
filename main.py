import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


if len(sys.argv) > 1:
    user_prompt = sys.argv[1]
    
    messages = [
    types.Content(role ='user', parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001', contents=messages
    )

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose" :
        print(response.text)
        usage = response.usage_metadata
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_tokens_details[0].token_count}")
    else:
        print(response.text)

else:
    print("please provide a prompt")
    sys.exit(1)
