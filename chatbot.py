import json
import random

class Chatbot:
    def __init__(self, data_file='chatbot_data.json', history_file='chat_history.txt'):

        self.data_file = data_file
        self.history_file = history_file
        self.responses = self.load_responses()
        self.chat_history = []

    def load_responses(self):
        # Load responses from JSON file
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
            return data['responses']
        except FileNotFoundError:
            return {}

    def save_responses(self):
        # Save updated responses back to JSON file
        with open(self.data_file, 'w') as file:
            json.dump({"responses": self.responses}, file, indent=4)

    def get_response(self, message):
        # Check if the response exists, else ask for a new one
        if message.lower() in self.responses:
            return random.choice(self.responses[message.lower()])
        else:
            new_response = input("\nI don't know how to respond to that. How should I respond?\n")
            self.responses[message.lower()] = new_response  # Update responses dictionary
            self.save_responses()  # Save updates to file
            return new_response

    def log_chat(self, message, response):
        # Log the conversation to history
        self.chat_history.append(f"You: {message}\nBot: {response}\n")

    def save_chat_history(self):
        # Save conversation history to a text file
        with open(self.history_file, 'a') as file:
            file.writelines(self.chat_history)
            print("Chat history has been saved. Goodbye!")

    def run(self):
        print("Welcome to the chatbot! Type 'quit' to exit.")
        try:
            while True:
                message = input("You: ")
                if message.lower() == "quit":
                    break
                response = self.get_response(message)
                print("Bot:", response)
                self.log_chat(message, response)

        except KeyboardInterrupt:
            print("\nCtrl+C detected! Exiting gracefully...")
        finally:
            self.save_chat_history()

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()
