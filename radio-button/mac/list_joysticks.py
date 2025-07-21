import pygame

pygame.init()
pygame.joystick.init()

print(f"Found {pygame.joystick.get_count()} joysticks.")
if pygame.joystick.get_count() == 0:
    print("No joysticks found. Make sure your flight stick is connected.")
else:
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print(f"\nJoystick {i}: {joystick.get_name()}")
        print(f"  Number of buttons: {joystick.get_numbuttons()}")
        print(f"  Number of axes: {joystick.get_numaxes()}")
        print(f"  Number of hats: {joystick.get_numhats()}")

    print("\nPress a button on your flight stick. Press Ctrl+C to exit.")
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    print(f"Button {event.button} pressed on joystick {event.joy}")
                elif event.type == pygame.JOYBUTTONUP:
                    print(f"Button {event.button} released on joystick {event.joy}")
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        pygame.quit()

