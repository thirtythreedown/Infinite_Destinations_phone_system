# TODO: Integrate LED functions

import RPi.GPIO as GPIO
import time
import pygame

# Set up GPIO
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the phone keypad
row_pins = [17, 27, 22, 5]  # Example GPIO pins for rows
col_pins = [6, 13, 19, 26]  # Example GPIO pins for columns

# Set up row pins as outputs
for pin in row_pins:
    GPIO.setup(pin, GPIO.OUT)

# Set up column pins as inputs with pull-up resistors
for pin in col_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define the keypad layout
keypad = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# Load audio files
offhook_sound = pygame.mixer.Sound("offhook.wav")
secret_sound = pygame.mixer.Sound("secret.wav")

# Variables to track phone state and input
phone_offhook = False
input_buffer = ""


def check_hook_state():
    # This function should check if the phone is off the hook
    # For simplicity, we'll use a GPIO pin to simulate this
    hook_pin = 21  # Example GPIO pin for hook state
    GPIO.setup(hook_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    return not GPIO.input(hook_pin)  # Assume low means off-hook


def scan_keypad():
    for row_num, row_pin in enumerate(row_pins):
        GPIO.output(row_pin, GPIO.LOW)
        for col_num, col_pin in enumerate(col_pins):
            if GPIO.input(col_pin) == GPIO.LOW:
                GPIO.output(row_pin, GPIO.HIGH)
                return keypad[row_num][col_num]
        GPIO.output(row_pin, GPIO.HIGH)
    return None


try:
    while True:
        current_hook_state = check_hook_state()

        if current_hook_state and not phone_offhook:
            # Phone just taken off the hook
            phone_offhook = True
            offhook_sound.play()
            print("Phone off hook, playing greeting")
        elif not current_hook_state and phone_offhook:
            # Phone just placed back on the hook
            phone_offhook = False
            pygame.mixer.stop()
            input_buffer = ""
            print("Phone on hook, stopping audio")

        if phone_offhook:
            key = scan_keypad()
            if key:
                input_buffer += key
                print(f"Key pressed: {key}")

                if input_buffer.endswith("111#"):
                    secret_sound.play()
                    print("Secret code entered, playing secret message")
                    input_buffer = ""  # Reset buffer after playing secret sound

        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()
    pygame.mixer.quit()
