import json

def load_responses():
    # Load responses from JSON file
    try:
        with open('chatbot_data.json', 'r') as file:
            data = json.load(file)
        return data['responses']
    except FileNotFoundError:
        return {}

def save_responses(responses):
    # Save updated responses back to JSON file
    with open('chatbot_data.json', 'w') as file:
        json.dump({"responses": responses}, file, indent=4)

def get_response(message, responses):
    # Check if the response exists, else ask for a new one
    if message.lower() in responses:
        return responses[message.lower()]
    else:
        new_response = input("I don't know how to respond to that. How should I respond?\n")
        responses[message.lower()] = new_response  # Update responses dictionary
        save_responses(responses)  # Save updates to file
        return new_response

def main():
    responses = load_responses()
    print("Welcome to the chatbot! Type 'quit' to exit.")
    chat_history = []

    while True:
        message = input("You: ")
        if message.lower() == "quit":
            break
        response = get_response(message, responses)
        print("Bot:", response)

        # Log the conversation to history
        chat_history.append(f"You: {message}\nBot: {response}\n")

    # Save conversation history to a text file
    with open('chat_history.txt', 'a') as file:
        file.writelines(chat_history)
        print("Chat history has been saved.")

if __name__ == "__main__":
    main()
