import speech_recognition
from fuzzywuzzy import process
import string
import pyttsx3

valid_answers = list(string.ascii_lowercase)
valid_words = ["learn", "test", "exit"] 
engine = pyttsx3.init()


def recognize_alphabet():
    recognizer = speech_recognition.Recognizer()
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic, timeout=5)
            text = recognizer.recognize_google(audio)
            text = text.lower()
            simplified_text = simplify(text)
            
            return simplified_text, True
    except (speech_recognition.UnknownValueError, speech_recognition.WaitTimeoutError):
        return "Sorry, please try again.", False
    
def simplify(text):
    words = text.split()
    last_word = words[-1]

    closest_match, similarity = process.extractOne(last_word, valid_answers)
    
    if similarity > 80:
        return closest_match
    else:
        return last_word
    
    

    
def recognize_word():
    recognizer = speech_recognition.Recognizer()
    print("Recognizing word...")
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic, timeout=5)
            text = recognizer.recognize_google(audio)
            text = text.lower()

            # Simplify the word to match only valid words
            simplified_word = simplify_word(text)
            return simplified_word, True
    except speech_recognition.UnknownValueError as e:
        print(f"Error: Could not understand audio. {e}")
        return "Sorry, please try again.", False
    except speech_recognition.WaitTimeoutError as e:
        print(f"Error: Listening timed out while waiting for phrase. {e}")
        return "Sorry, please try again.", False
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return "Sorry, please try again.", False
    

def simplify_word(text):
    words = text.split()
    last_word = words[-1]  # Take the last word spoken
    closest_match, similarity = process.extractOne(last_word, valid_words)
    print(f"Input: {last_word}, Match: {closest_match}, Similarity: {similarity}%")  # Debugging line

    if similarity > 80:  # Accept only high-confidence matches
        return closest_match
    else:
        return "Invalid word"
    
    

def say(something):
    engine.say(something)
    engine.runAndWait()