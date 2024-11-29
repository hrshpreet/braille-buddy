import speech_recognition
from fuzzywuzzy import process
import string


def recognize_word():
    # take audio input, process and return
    ans = input("the student said:")
    return ans

def recognize_alphabet():
    valid_answers = list(string.ascii_lowercase)
    
    return 0

def say(something):
    print("echo: ", something)