import sys
import os

if os.name == "posix":
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
else:
    GPIO = None
    
def set_pin_high(pin):
    if GPIO:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)
    else:
        print(f"Pin {pin} is HIGH")
        
def set_pin_low(pin):
    if GPIO:
        GPIO.output(pin, False)
    else:
        print(f"Pin {pin} is LOW")
        
def print_alphabet(alphabet):
    print("The screen shows: ", alphabet)
def hide_alphabet(alphabet):
    print("The screen is neutral")