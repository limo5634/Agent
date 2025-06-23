import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.call_function import *


system_prompt = """
Du bist ein hilfreicher KI-Coding-Assistent. Folge diesen Regeln:
1. Analysiere Probleme Schritt für Schritt
2. Verwende Funktionen um Daten zu sammeln
3. Denke laut nach bevor du handelst
4. Überprüfe Änderungen mit Tests
"""




def main():
    load_dotenv()

    args = sys.argv[1:]
    print("System prompt:", system_prompt)

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
    MAX_ITERATIONS = 20
    messages_history = messages.copy()  # Kopie der initialen Nachrichten

    for iteration in range(MAX_ITERATIONS):
        if verbose:
            print(f"\n--- Iteration {iteration+1}/{MAX_ITERATIONS} ---")

        # API-Aufruf mit gesamter Historie
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages_history,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )

        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Füge Modellantwort zur Historie hinzu
        if response.candidates:
            model_response = response.candidates[0].content
            messages_history.append(model_response)

            if verbose:
                print(f"Model response: {model_response}")

        # Verarbeite Funktionsaufrufe
        if response.function_calls:
            for function_call_part in response.function_calls:
                # Funktion ausführen
                function_call_result = call_function(function_call_part, verbose=verbose)
                
                # Prüfe Ergebnis
                if not function_call_result.parts or not hasattr(function_call_result.parts[0], "function_response"):
                    raise RuntimeError("Invalid function response structure")
                
                # Füge Ergebnis zur Historie hinzu
                messages_history.append(function_call_result)
                
                if verbose:
                    response_data = function_call_result.parts[0].function_response.response
                    print(f"-> Function result: {response_data}")
        else:
            # Keine weiteren Aktionen -> Ausgabe und Ende
            print("\nFinal response:")
            print(response.text)
            return

    print(f"\nStopped after {MAX_ITERATIONS} iterations")




if __name__ == "__main__":
    main()
