import json
import random
import logging
import pyttsx3
from gtts import gTTS
import os
import playsound
import speech_recognition as sr
import socket
from fuzzywuzzy import process

def is_connected(hostname="8.8.8.8", port=53, timeout=3):
    """
    Check network connectivity by trying to connect to Google's DNS server.
    This server is chosen for its high availability.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((hostname, port))
        return True
    except socket.error as ex:
        print("No internet connection:", ex)
        return False

class Chatbot:
    def __init__(self, data_file='chatbot_data.json', history_file='chat_history.txt'):
        self.data_file = data_file
        self.history_file = history_file
        self.responses = self.load_responses()
        self.chat_history = []
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        logging.basicConfig(filename='chatbot.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Chatbot started.")



    def load_responses(self):
        
        print("Loading responses")
        # Load responses from JSON file
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
            return data['responses']
        except FileNotFoundError:
            logging.error("Response data file not found.")
            return {}
        except json.JSONDecodeError:
            logging.error(f"JSONDecodeError: {self.data_file} could not be decoded.")
            return {}
        except Exception as e:
            logging.error(f"Unexpected error when loading responses: {e}")
            return {}


    def save_responses(self):
        # Save updated responses back to JSON file
        try:
            with open(self.data_file, 'w') as file:
                json.dump({"responses": self.responses}, file, indent=4)
        except Exception as e:
            logging.error(f"Failed to save responses: {e}")


    # def get_response(self, message):
    #     print("Message received in get_response function: {}".format(message))
    #     # Search through existing categories for a keyword match
    #     for category, content in self.responses.items():
    #         if message in content['keywords']:
    #             return random.choice(content['responses'])

    #     # If no existing response is found, ask the user for a new response and details
    #     print("\nI don't know how to respond to that. Let's add a new response.")
    #     new_response = input("How should I respond to '{}'?\n".format(message))
    #     new_category = input("Enter a category for this response (existing or new):\n")
    #     new_keywords = input("Enter keywords for this response, separated by commas (include your original input):\n").split(',')

    #     # Clean up keyword input
    #     new_keywords = [keyword.strip().lower() for keyword in new_keywords]

    #     # Check if the category already exists, if not, create a new category
    #     if new_category in self.responses:
    #         # Add new keywords to the category's keywords and avoid duplicates
    #         self.responses[new_category]['keywords'] = list(set(self.responses[new_category]['keywords'] + new_keywords))
    #         # Add the new response
    #         self.responses[new_category]['responses'].append(new_response)
    #     else:
    #         # Create a new category with the new keywords and response
    #         self.responses[new_category] = {'keywords': new_keywords, 'responses': [new_response]}

    #     # Save the updated responses to the JSON file
    #     self.save_responses()

    #     return new_response


    def get_response(self, message):
        print("Message received in get_response function: {}".format(message))
        highest_score = 0
        best_match_category = None

        # Iterate over each category to find the best match using fuzzy string matching
        for category, content in self.responses.items():
            # Find the best match within the current category's keywords
            match, score = process.extractOne(message, content['keywords'])
            
            # Check if this category's best score is higher than what we have found so far
            if score > highest_score:
                highest_score = score
                best_match_category = category

        # If a reasonable match is found (you can adjust the threshold as needed)
        if highest_score > 60:  # 60 is an example threshold
            # Return a random response from the best match category
            return random.choice(self.responses[best_match_category]['responses'])
        
        # If no good match is found, ask the user to define the response
        print("\nI don't know how to respond to that. Let's add a new response.")
        new_response = input("How should I respond to '{}'?\n".format(message))
        new_category = input("Enter a category for this response (existing or new):\n")
        new_keywords = input("Enter keywords for this response, separated by commas (include your original input):\n").split(',')
        new_keywords = [keyword.strip().lower() for keyword in new_keywords]

        # Update the responses dictionary
        if new_category in self.responses:
            self.responses[new_category]['keywords'].extend(new_keywords)
            self.responses[new_category]['responses'].append(new_response)
        else:
            self.responses[new_category] = {'keywords': new_keywords, 'responses': [new_response]}
        
        # Save the updated responses to the JSON file
        self.save_responses()

        return new_response



    def log_chat(self, message, response):
        # Log the conversation to history
        self.chat_history.append(f"You: {message}\nBot: {response}\n")


    def save_chat_history(self):
        """Save conversation history to a text file."""
        try:
            with open(self.history_file, 'a') as file:
                file.writelines(self.chat_history)
            logging.info("Chat history has been saved.")
        except Exception as e:
            logging.error(f"Failed to save chat history: {e}")
            
    def speak(self, text):
        """Speak the response using gTTS or pyttsx3 based on internet connectivity."""
        print("text received : {}".format(text))
        if is_connected():
            try:
                tts = gTTS(text=text, lang='en')
                path = "response.mp3"
                tts.save(path)
                playsound.playsound(path)
                os.remove(path)
            except Exception as e:
                logging.error(f"gTTS failed: {e}")
                self.engine.say(text)
                self.engine.runAndWait()
        else:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen(self):
        
        print('\nListening...')
        self.recognizer.dynamic_energy_threshold = True  # Consider allowing dynamic adjustments
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust the duration to better suit the environment noise level
            try:
                # Listen for a single phrase. Increasing timeout and phrase_time_limit might help
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                print('\nProcessing...')
            except sr.WaitTimeoutError:
                logging.error("Listening timed out whilst waiting for phrase to start")
                print("No speech detected within the time limit.")
                return None

        # Recognize speech using Google's speech recognition service
        try:
            said = self.recognizer.recognize_google(audio)
            print(f"\nUser said: {said}")
            return said.lower()
        except sr.UnknownValueError:
            logging.error("I couldn't understand what you said. Please try again.")
            # print("I couldn't understand what you said.")
        except sr.RequestError as e:
            logging.error(f"Could not request results from the speech recognition service; {e}")
            # print("Network error.")
        except Exception as e:
            logging.error(str(e))
            # print("An error occurred: " + str(e))

        return None
        
        
        # ------------<<<<<>>>>>>>>>>>>>>>>>------------ old version below --------------------
        
        # print('\nListening...')
        # self.recognizer.dynamic_energy_threshold = False
        # self.recognizer.energy_threshold = 4000
        # with self.microphone as source:
        #     self.recognizer.adjust_for_ambient_noise(source)
        #     audio = self.recognizer.listen(source,phrase_time_limit=5)
        #     print('\nProcessing...')
        #     said = ""
        #     try:
        #         said = self.recognizer.recognize_google(audio)
        #         print(f"\nUser said: {said}")
                
        #     except sr.WaitTimeoutError:
        #         #Error recognizer timed out whilst waiting for phrase to start
        #         logging.error("Listening timed out whilst waiting for phrase to start")
        #         return None
            
        #     except sr.UnknownValueError:
        #         # Error: recognizer could not understand the audio
        #         logging.error("I couldn't understand what you said. Please try again.")
        #         return None
            
        #     except sr.RequestError as e:
        #         # Error: Could not request results from Google Speech Recognition service
        #         logging.error(f"Could not request results from the speech recognition service; {e}")
        #         return None
                
        #     except Exception as e:
        #         logging.error(e)
        #         # speak("I didn't get it, Say that again please...")
        #         if "connection failed" in str(e):
        #             # speak("Your System is Offline...", True, True)
        #             logging.error("Your System is Offline...")
        #         return None
        # return said.lower()
        
        
        
        
            
            

    def run(self):
        try:
            while True:
                
                if is_connected():
                    spoken_text = self.listen()
                    if spoken_text == "quit":
                        break
                    if spoken_text is None:
                        continue
                else:
                    print("No internet connection, switching to text input:")
                    spoken_text = input("You: ").lower()
                    if "quit" in spoken_text:
                        break

                response = self.get_response(spoken_text)
                self.speak(response)
                self.log_chat(spoken_text, response)
                
                
                # message = input("You: ").lower()
                # if message == "quit":
                #     logging.info(f"program quit")
                #     break
                # response = self.get_response(message)
                # print("Bot:", response)
                # self.log_chat(message, response)

        except KeyboardInterrupt:
            logging.info(f"program quit CTRL+C detected")
        finally:
            self.save_chat_history()

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()
