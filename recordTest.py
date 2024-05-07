import speech_recognition as sr

def record():
    print('Listening...')
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(f"User said: {said}")
        except Exception as e:
            print(f"Error: {e}")
            return 'None'
    return said.lower()

if __name__ == "__main__":
    while True:
        print(record())