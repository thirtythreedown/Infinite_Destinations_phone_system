import RPi.GPIO as GPIO
import time
import select
import sys
import tty
import termios

# Define GPIO pin for hook switch
HOOK_SWITCH_PIN = 14  # Updated to GPIO pin 14

def setup():
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(HOOK_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up hook switch with pull-up resistor

def is_on_hook():
    # Check if the phone is on the hook (switch is closed)
    return GPIO.input(HOOK_SWITCH_PIN) == GPIO.LOW

def is_off_hook():
    # Check if the phone is off the hook (switch is open)
    return not is_on_hook()

def get_key_non_blocking():
    # Use non-blocking input to check for key presses
    dr, dw, de = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None

def handle_input():
    print("Phone is off-hook. Waiting for key input...")

    while is_off_hook():  # Keep checking if phone is still off-hook
        key = get_key_non_blocking()  # Check for key press

        if key:
            if key == '1':
                print("Option 1 selected.")
            elif key == '2':
                print("Option 2 selected.")
            elif key == '3':
                print("Option 3 selected.")
            else:
                print("Invalid option.")

        if is_on_hook():
            print("Receiver placed back on hook. Exiting input handler...")
            return  # Exit the function to return to waiting mode

        time.sleep(0.1)  # Small delay to reduce CPU usage

def main():
    setup()
    print("Waiting for phone to go off-hook...")

    try:
        while True:
            if is_off_hook():
                print("Phone is off-hook!")
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
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
