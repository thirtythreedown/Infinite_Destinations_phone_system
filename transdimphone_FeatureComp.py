# TO DO: Pygame audio

import RPi.GPIO as GPIO
import time
import select
import sys
import tty
import termios
import pygame
import numpy as np

# Initialize pygame mixer for mono output
pygame.mixer.pre_init(frequency=8000, size=-16, channels=1, buffer=1024, allowedchanges=0)
pygame.mixer.init()

# Define GPIO pin for hook switch
HOOK_SWITCH_PIN = 14  # GPIO connected to the phone hook

def setup():
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(HOOK_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up hook switch with pull-up resistor

    for pin in row_pins:
        GPIO.setup(pin, GPIO.OUT)

    for pin in col_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define the GPIO pins for rows and columns on the keypad
row_pins = [23, 24, 25, 16]  # GPIO pins connected to rows
col_pins = [17, 27, 22]  # GPIO pins connected to columns

# Set up the GPIO pins states for the keypad


# Define the keypad layout
keypad = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

# DTMF frequencies
row_frequencies = [697, 770, 852, 941]
col_frequencies = [1209, 1336, 1477]

def is_on_hook():
    # Check if the phone is on the hook (switch is closed)
    return GPIO.input(HOOK_SWITCH_PIN) == GPIO.LOW

def is_off_hook():
    # Check if the phone is off the hook (switch is open)
    return not is_on_hook()

# def scan_keypad():
#     for row, row_pin in enumerate(row_pins):
#         GPIO.output(row_pin, GPIO.LOW)
#
#         for col, col_pin in enumerate(col_pins):
#             if GPIO.input(col_pin) == GPIO.LOW:
#                 GPIO.output(row_pin, GPIO.HIGH)
#                 return keypad[row][col]
#
#         GPIO.output(row_pin, GPIO.HIGH)
#
#     return None

def scan_keypad():
    for row, row_pin in enumerate(row_pins):
        GPIO.output(row_pin, GPIO.LOW)

        for col, col_pin in enumerate(col_pins):
            if GPIO.input(col_pin) == GPIO.LOW:
                GPIO.output(row_pin, GPIO.HIGH)
                return keypad[row][col], row, col

        GPIO.output(row_pin, GPIO.HIGH)

    return None, None, None

def generate_dtmf_tone(row, col):
    duration = 0.5  # Duration of the tone in seconds
    sample_rate = 8000  # Sample rate in Hz
    t = np.linspace(0, duration, int(duration * sample_rate), False)

    tone = np.sin(2 * np.pi * row_frequencies[row] * t) + np.sin(2 * np.pi * col_frequencies[col] * t)
    tone = np.int16(tone / np.max(np.abs(tone)) * 32767)

    return pygame.sndarray.make_sound(tone)

# Pre-generate all DTMF tones
dtmf_tones = {}
for row in range(4):
    for col in range(3):
        dtmf_tones[(row, col)] = generate_dtmf_tone(row, col)

def get_key_non_blocking():
    # Use non-blocking input to check for key presses
    dr, dw, de = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None

def play_sound(file):
    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)  # Wait until the sound has finished playing
    except Exception as e:
        print(f"Error playing sound: {e}")

def handle_input():
    print("Waiting for input...")
    print("\nPlease select from the following options to begin your travel experience.")
    print("\nFor our top 3 destinations, press 1.")
    print("\nFor essential travel precautions, press 2.")
    print("\nTo book your next travel adventure, press 3.")
    play_sound("transdimphone_audio_US/transdimphone_menu.mp3")

    while is_off_hook():  # Keep checking if phone is still off-hook
        key, row, col = scan_keypad() #Getting key presses from the keypad
        # key = get_key_non_blocking()  # Check for key press

        if key:
            if (row, col) in dtmf_tones:
                dtmf_tones[(row, col)].play()

            if key == '1':
                print("Top destinations")
                play_sound("transdimphone_audio_US/transdimphone_destinations.mp3")
                return

            elif key == '2':
                print("Traveling precautions")
                play_sound("transdimphone_audio_US/transdimphone_precautions.mp3")
                return

            elif key == '3':
                print("Booking your travel")
                play_sound("transdimphone_audio_US/transdimphone_booking.mp3")
                return

            else:
                print("Invalid option.")
                play_sound("transdimphone_audio_US/transdimphone_invalid.mp3")
                return

        time.sleep(0.3)  # Small delay to reduce CPU usage

        if is_on_hook():
            print("Receiver placed back on hook. Exiting input handler...")
            return  # Exit the function to return to waiting mode

        time.sleep(0.3)  # Small delay to reduce CPU usage

def main():
    setup()
    print("Waiting for phone to go off-hook...")

    try:
        while True:
            if is_off_hook():
                print("Phone is off-hook!")
                print("Welcome to Infinite Destinations Travel Co.,")
                print("\nwhere the journey never ends. Our team is here to make your adventures in the past, present, future, and alternate universes unforgettable.")
                time.sleep(2)
                play_sound("transdimphone_audio_US/transdimphone_welcome.mp3")
                handle_input()  # Start the input handler
                print("Returned to main loop. Waiting for phone to go off-hook again...")
            else:
                print("Phone is on-hook.")

            time.sleep(0.1)  # Small delay to reduce CPU usage
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

if __name__ == "__main__":
    # Prepare for non-blocking key input
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        main()
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)  # Restoring the state of the terminal

