import ollama

print("Ollama Python library (v0.6.1) imported successfully!\n")

# List available models with better error handling
try:
    response = ollama.list()
    if 'models' not in response or not response['models']:
        print("No models found—pull one with 'ollama pull llama3.1:8b' if needed.")
    else:
        print("Available models on your Ollama server:")
        for model in response['models']:
            name = model.get('name', 'Unknown')
            size_gb = model.get('size', 0) / 1_000_000_000
            print(f"- {name} (size: ~{size_gb:.1f} GB)")
except Exception as e:
    print("Could not connect to Ollama server:")
    print(f"Error: {e}")
    print("\nFix: Start the Ollama app/tray icon. It must be running for the Python library to work.")
    print("Once started, rerun this script.")

# Inference test (only if server connected)
try:
    chat_resp = ollama.chat(
        model='llama3.1:8b',
        messages=[{'role': 'user', 'content': 'Briefly explain how journaling supports psychological healing.'}]
    )
    print("\nServer connection successful! Sample response:")
    print(chat_resp['message']['content'])
except Exception as e:
    print("\nChat test skipped due to server connection issue.")
    print(f"(Error details: {e})")