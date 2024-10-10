import RPi.GPIO as GPIO
import time

# Define GPIO pin for hook switch
HOOK_SWITCH_PIN = 14  # Updated to GPIO pin 14

def setup():
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(HOOK_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up hook switch with pull-up resistor

def is_off_hook():
    # Check if the phone is off the hook (switch is pressed)
    return GPIO.input(HOOK_SWITCH_PIN) == GPIO.LOW

def main():
    setup()
    print("Waiting for phone to go off-hook...")

    try:
        while True:
            if is_off_hook():
                print("Phone is off-hook!")
                # Trigger main menu or other functions here
                while is_off_hook():
                    # Continuously check if the phone is still off-hook
                    time.sleep(0.1)  # Small delay to reduce CPU usage

                # If the receiver is placed back on-hook, exit the loop and return to waiting mode
                print("Phone is back on-hook. Returning to waiting mode...")
            else:
                print("Phone is on-hook.")

            time.sleep(0.1)  # Small delay to reduce CPU usage
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

if __name__ == "__main__":
    main()
