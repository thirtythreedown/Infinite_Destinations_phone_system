# TO DO: ADD EXCEPTION FOR MULTIPLE PRESSES AT THE SAME TIME

import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for rows and columns
row_pins = [23, 24, 25, 16]  # GPIO pins connected to rows
col_pins = [17, 27, 22]  # GPIO pins connected to columns

# Define the keypad layout
keypad = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

# Set up the GPIO pins
for pin in row_pins:
    GPIO.setup(pin, GPIO.OUT)

for pin in col_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def scan_keypad():
    for row, row_pin in enumerate(row_pins):
        GPIO.output(row_pin, GPIO.LOW)

        for col, col_pin in enumerate(col_pins):
            if GPIO.input(col_pin) == GPIO.LOW:
                GPIO.output(row_pin, GPIO.HIGH)
                return keypad[row][col]

        GPIO.output(row_pin, GPIO.HIGH)

    return None


try:
    print("Keypad Test: Press keys on the keypad. Press Ctrl+C to exit.")
    while True:
        key = scan_keypad()
        if key is not None:
            print(f"Key Pressed: {key}")
            time.sleep(0.3)  # Debounce delay
        time.sleep(0.05)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("\nKeypad test terminated.")

finally:
    GPIO.cleanup()
