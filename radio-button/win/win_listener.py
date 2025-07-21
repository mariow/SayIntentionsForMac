import socket
import vgamepad as vg # Import the vgamepad library
import time

# --- Configuration ---
LISTEN_IP = "0.0.0.0" # Listen on all available interfaces
LISTEN_PORT = 50000   # <--- Must match TARGET_PORT from macOS sender script
MESSAGE_BUTTON_DOWN = "FLIGHTSTICK_BUTTON_DOWN" # Must match macOS sender script
MESSAGE_BUTTON_UP = "FLIGHTSTICK_BUTTON_UP"     # Must match macOS sender script

# --- Setup ViGEmBus Virtual Gamepad ---
gamepad = vg.VX360Gamepad()
print("Virtual Xbox 360 Gamepad created.")

print(dir(vg.XUSB_BUTTON))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket
sock.bind((LISTEN_IP, LISTEN_PORT))
sock.settimeout(0.5) # Timeout for non-blocking receive

print(f"Listening for UDP messages on {LISTEN_IP}:{LISTEN_PORT}")
print(f"Expecting messages: '{MESSAGE_BUTTON_DOWN}' and '{MESSAGE_BUTTON_UP}'")
print("Will simulate A button on virtual Xbox 360 Gamepad.")

# --- Main Loop ---
try:
    while True:
        try:
            data, addr = sock.recvfrom(1024) # Buffer size 1024 bytes
            received_message = data.decode('utf-8')

            # print(f"Received message: '{received_message}' from {addr}") # Uncomment for verbose debugging

            if received_message == MESSAGE_BUTTON_DOWN:
                print(f"Button DOWN message received. Pressing virtual gamepad A button...")
                # CORRECTED LINE HERE: Try vg.XUSB_BUTTON.XUSB_BUTTON_A
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.update()
            elif received_message == MESSAGE_BUTTON_UP:
                print(f"Button UP message received. Releasing virtual gamepad A button...")
                # CORRECTED LINE HERE: Try vg.XUSB_BUTTON.XUSB_BUTTON_A
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.update()

        except socket.timeout:
            pass
        except Exception as e:
            print(f"An error occurred during UDP receive or gamepad control: {e}")
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nExiting.")
finally:
    print("Closing UDP listener and releasing virtual gamepad buttons.")
    gamepad.release_all()
    gamepad.update()
    sock.close()
