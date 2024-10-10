import RPi.GPIO as GPIO
import time
import pygame
import getkey

# Define GPIO pin for hook switch
HOOK_SWITCH_PIN = 14  # Updated to GPIO pin 14

def setup():
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(HOOK_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up hook switch with pull-up resistor

def is_off_hook():
    # Check if the phone is off the hook (switch is pressed)
    return GPIO.input(HOOK_SWITCH_PIN) == GPIO.LOW

# Initialize pygame mixer for playing sound
pygame.mixer.init()

def play_sound(file):
    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)  # Wait until the sound has finished playing
    except Exception as e:
        print(f"Error playing sound: {e}")

def handle_input():
    while is_off_hook():  # Keep checking if phone is still off-hook
        print("\nPlease select from the following options to begin your travel experience.")
        print("\nFor our top 3 destinations, press 1.")
        print("\nFor essential travel precautions, press 2.")
        print("\nTo book your next travel adventure, press 3.")

        # Check if the receiver is back on the hook before waiting for input
        if not is_off_hook():
            print("Receiver placed back on hook. Returning to waiting mode...")
            return  # Exit the function to return to waiting mode

        key = getkey.getkey()

        if key == '1':
            print("You've chosen to explore our top destinations through time and space!")
            # Detailed messages...
        elif key == '2':
            print("Precautions for your journey:")
            # Precautions details...
        elif key == '3':
            print("Booking a Time Travel Destination:")
            # Booking details...
        else:
            print("I'm sorry, I didn't catch that. Please press 1, 2, or 3 to continue.")
            #play_sound("invalid_input.wav")
            continue  # Loop back to the main menu

        print("\nReturning to the main menu...")
        time.sleep(2)  # Short delay before returning to the main menu

        # Check if the receiver is back on the hook before continuing the loop
        if not is_off_hook():
            print("Receiver placed back on hook. Returning to waiting mode...")
            return  # Exit the function to return to waiting mode

def main():
    setup()
    print("Waiting for phone to go off-hook...")

    try:
        while True:
            if is_off_hook():
                print("Phone is off-hook!")
                # Greet the user
                print("Welcome to Infinite Destinations Travel Co., where the journey never ends.")
                #play_sound("greeting_and_options.wav")

                time.sleep(2)  # Simulate a delay while waiting for input

                handle_input()  # Start the input handler

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
