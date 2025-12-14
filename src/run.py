from engine import respond

if __name__ == "__main__":
    print("Healing Vault is running. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        reply = respond(user_input)
        print("\nGuide:", reply, "\n")
