from app.app import process_request

def main():
    print("AI Agent Active. (Type 'exit' ,'q' to quit)")
    while True:
        user_input = input("Enter Your Prompt : ").strip()
        if user_input.lower() in ['exit','quit','q']:
            print("AI Agent: Goodbye!")
            break

        if user_input.lower() in ['clear','cls']:
            print("\033c", end="")  # Clear console
            continue
        
        if not user_input:
            print("AI Agent: Please enter a valid prompt.")
            continue

        response = process_request(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()







