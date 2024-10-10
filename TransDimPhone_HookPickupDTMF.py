import RPi.GPIO as GPIO
import time
import pygame
import numpy as np

# Initialize pygame mixer
pygame.mixer.init(frequency=8000, size=-16, channels=1, buffer=1024)

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for keypad rows and columns
row_pins = [23, 24, 25, 16]  # GPIO pins connected to rows
col_pins = [17, 27, 22]  # GPIO pins connected to columns

# Define the hook pin
HOOK_PIN = 14  # GPIO pin for hook state

# These pins are selected to not clash with any PWM or I2C pins

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

# Set up the GPIO pins
for pin in row_pins:
    GPIO.setup(pin, GPIO.OUT)

for pin in col_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(HOOK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def generate_dtmf_tone(row, col):
    duration = 0.1  # Duration of the tone in seconds
    sample_rate = 44100  # Sample rate in Hz
    t = np.linspace(0, duration, int(duration * sample_rate), False)

    tone = np.sin(2 * np.pi * row_frequencies[row] * t) + np.sin(2 * np.pi * col_frequencies[col] * t)
    tone = np.int16(tone / np.max(np.abs(tone)) * 32767)

    tone = tone.reshape((-1))  # Reshape as per your successful modification

    return pygame.sndarray.make_sound(tone)


def scan_keypad():
    for row, row_pin in enumerate(row_pins):
        GPIO.output(row_pin, GPIO.LOW)

        for col, col_pin in enumerate(col_pins):
            if GPIO.input(col_pin) == GPIO.LOW:
                GPIO.output(row_pin, GPIO.HIGH)
                return row, col

        GPIO.output(row_pin, GPIO.HIGH)

    return None, None


# Pre-generate all DTMF tones
dtmf_tones = {}
for row in range(4):
    for col in range(3):
        dtmf_tones[(row, col)] = generate_dtmf_tone(row, col)

# Load pre-recorded message
greeting_sound = pygame.mixer.Sound("64488^hellodar.mp3")  # Make sure this file exists in the same directory

try:
    print("Phone System Active: Waiting for off-hook. Press Ctrl+C to exit.")
    phone_offhook = False

    while True:
        current_hook_state = GPIO.input(HOOK_PIN) == GPIO.LOW  # Assume low means off-hook

        if current_hook_state and not phone_offhook:
            # Phone just taken off the hook
            phone_offhook = True
            print("Phone off hook, playing greeting")
            greeting_sound.play()

            # Wait for the greeting to finish
            while pygame.mixer.get_busy():
                time.sleep(0.1)

            print("Waiting for keypad input...")

        elif not current_hook_state and phone_offhook:
            # Phone just placed back on the hook
            phone_offhook = False
            print("Phone on hook")

        if phone_offhook:
            row, col = scan_keypad()
            if row is not None and col is not None:
                key = keypad[row][col]
                print(f"Key Pressed: {key}")

                # Play DTMF tone
                dtmf_tones[(row, col)].play()
                time.sleep(0.3)  # Debounce delay

        time.sleep(0.05)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("\nPhone system terminated.")

finally:
    pygame.mixer.quit()
    GPIO.cleanup()