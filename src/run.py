from engine import respond

def main():
    print("Healing Vault is running.")
    user_name = input("What would you like to be called? ").strip()

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Session ended.")
            break

        response = respond(user_input, user_name=user_name)
        print("\nResponse:\n")
        print(response)
        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    main()
