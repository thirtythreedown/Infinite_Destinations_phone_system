#import pygame
import time

# Initialize pygame mixer for playing sound
#pygame.mixer.init()


# Function to play a sound file
# def play_sound(file):
#     pygame.mixer.music.load(file)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         time.sleep(0.1)  # Wait until the sound has finished playing


# Function to handle user input and play the appropriate message
def handle_input():
    while True:
        print("\nPlease press 1, 2, 3, or 4 to select an option.")
        key = input("Enter your choice: ")

        if key == '1':
            print("You've chosen to explore our top destinations through time and space!")
            print(
                "1. **Alternate Paris, 1990:** Step into a GiscardPunk universe where President Giscard d'Estaing wins a second term, ushering in a glorious yet authoritarian era.")
            print(
                "2. **66 Million Years Ago:** Witness the cataclysmic asteroid impact in the Chicxulub area that wiped out 75% of Earth's animal population.")
            print(
                "3. **End of the Universe:** Travel to the ultimate frontier and experience the mysterious and breathtaking conclusion of everything.")
            # play_sound("destinations_message.wav")
        elif key == '2':
            print("Precautions for your journey:")
            print(
                "1. **Cultural Respect:** When visiting new cultures, always be respectful, ethical, and aware of local customs and norms. Your conduct reflects not only on yourself but on all travelers.")
            print(
                "2. **Health and Food Safety:** Be cautious of diseases and strange foods. This includes the peculiar concept of schadenfreude as a delicacy and avoiding anything in the color puce, which could have unpredictable effects.")
            print(
                "3. **No Organic Souvenirs:** Under no circumstances should you bring back organic matter from your trip. The consequences could be catastrophic, including temporal paradoxes or ecological disasters.")
            # play_sound("precautions_message.wav")
        elif key == '3':
            print("About ChronoVenture Time and Space Travel Agency:")
            print(
                "Founded by a legendary couple of grassroots inventors, ChronoVenture was born from their success in pizza rehydration technology and water purification. Their fortune allowed them to make time travel possible for everyone.")
            print(
                "Now retired to a small farm in the late 21st century Midwest, their legacy lives on through the dedicated staff of our agency, continuing their mission to make history and the future accessible to all.")
            # play_sound("agency_info_message.wav")
        elif key == '4':
            print("Booking a Time Travel Destination:")
            print(
                "We regret to inform you that due to temporal instability in your current time period, the reality you are experiencing is teetering between timelines.")
            print("As a result, we cannot process your booking at this moment. Please try again at a later date!")
            # play_sound("temporal_instability_message.wav")
        else:
            print("I'm sorry, I didn't catch that. Please press 1, 2, 3, or 4 to continue.")
            # play_sound("invalid_input.wav")
            continue  # Loop back to the main menu

        print("\nReturning to the main menu...")
        # play_sound("return_to_main_menu.wav")
        time.sleep(2)  # Short delay before returning to the main menu


# Main function to simulate the IVR system
def main():
    print("Welcome to ChronoVenture Time and Space Travel Agency!")
    # play_sound("greeting_and_options.wav")

    # Simulate a delay while waiting for input
    time.sleep(2)

    handle_input()


if __name__ == "__main__":
    main()
