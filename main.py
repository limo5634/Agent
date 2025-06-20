import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    load_dotenv()

    args = sys.argv[1:]

    # Check for verbose flag first
    verbose = False
    if '--verbose' in args:
        verbose = True
        args.remove('--verbose')

    # Check if we have a prompt after removing verbose flag
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?" --verbose')
        sys.exit(1)

    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose, user_prompt)


def generate_content(client, messages, verbose, user_prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
