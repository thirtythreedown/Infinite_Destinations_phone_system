import pygame
import numpy as np
import time

# Initialize pygame mixer for mono output
pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=1024, allowedchanges=0)
pygame.mixer.init()

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
def generate_dtmf_tone(row, col):
    duration = 0.5  # Duration of the tone in seconds
    sample_rate = 44100  # Sample rate in Hz
    t = np.linspace(0, duration, int(duration * sample_rate), False)

    tone = np.sin(2 * np.pi * row_frequencies[row] * t) + np.sin(2 * np.pi * col_frequencies)
    tone = np.int16(tone / np.max(np.abs(tone)) * 32767)
    # Reshape the array to match mono sound)
    tone = tone.reshape(-1)

    return pygame.sndarray.make_sound(tone)

# Generate all DTMF tones
dtmf_tones = {}
for row in range(4):
    for col in range(3):
        dtmf_tones[(row, col)] = generate_dtmf_tone(row, col)
def play_all_tones():
    for row in range(4):
        for col in range(3):
            key = keypad[row][col]
            print(f"Playing tone for key: {key}")
            dtmf_tones[(row, col)].play()
            pygame.time.wait(1000)  # Wait for 1 second
            pygame.mixer.stop()  # Stop the current tone
            time.sleep(0.5)  # Half second break between tones

try:
    print("Playing all DTMF tones in order. Press Ctrl+C to stop.")
    play_all_tones()
    print("All tones played.")
except KeyboardInterrupt:
    print("\nPlayback stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    pygame.mixer.quit()
    print("Pygame mixer closed.")
