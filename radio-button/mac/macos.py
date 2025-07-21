import pygame
import socket
import time

# --- Configuration ---
TARGET_WINDOWS_IP = "10.211.55.3"  # <--- REPLACE with your Windows VM's IP (e.g., 10.211.55.101)
TARGET_PORT = 50000               # <--- Must match Windows listener port
JOYSTICK_INDEX = 1                # <--- REPLACE with the index from list_joysticks.py
BUTTON_INDEX_TO_FORWARD = 0       # <--- REPLACE with the button index from list_joysticks.py
MESSAGE_BUTTON_DOWN = "FLIGHTSTICK_BUTTON_DOWN" # Message for press
MESSAGE_BUTTON_UP = "FLIGHTSTICK_BUTTON_UP"     # Message for release

# --- Setup ---
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joysticks found. Exiting.")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(JOYSTICK_INDEX)
joystick.init()
print(f"Monitoring '{joystick.get_name()}' (Joystick {JOYSTICK_INDEX}) for button {BUTTON_INDEX_TO_FORWARD}.")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket

# --- Main Loop ---
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN and event.joy == JOYSTICK_INDEX:
                if event.button == BUTTON_INDEX_TO_FORWARD:
                    print(f"Button {BUTTON_INDEX_TO_FORWARD} pressed. Sending '{MESSAGE_BUTTON_DOWN}'...")
                    sock.sendto(MESSAGE_BUTTON_DOWN.encode('utf-8'), (TARGET_WINDOWS_IP, TARGET_PORT))
            elif event.type == pygame.JOYBUTTONUP and event.joy == JOYSTICK_INDEX:
                if event.button == BUTTON_INDEX_TO_FORWARD:
                    print(f"Button {BUTTON_INDEX_TO_FORWARD} released. Sending '{MESSAGE_BUTTON_UP}'...")
                    sock.sendto(MESSAGE_BUTTON_UP.encode('utf-8'), (TARGET_WINDOWS_IP, TARGET_PORT))
        time.sleep(0.01) # Small delay to reduce CPU usage
except KeyboardInterrupt:
    print("\nExiting.")
finally:
    sock.close()
    pygame.quit()

