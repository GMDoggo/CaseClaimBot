from pyautogui import *
import pyautogui
import time
import keyboard
import numpy as np
import random
import win32api, win32con

# Define how it will click on a case
def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

while keyboard.is_pressed('right') == False:
    # Reset the flag variable for each iteration of the outer loop
    claim_button_found = False

    # Check for the exact color at (490, 550)
    pixel_color = pyautogui.pixel(490, 550)
    if pixel_color == (26, 30, 40):
        # If case is visible, click it
        click(490, 550)
        # Give enough time for the tab to load
        time.sleep(1)

        while not claim_button_found:
            try:
                # Look for the claimcase.png on screen
                claim_button_location = pyautogui.locateOnScreen('claimcase.png', grayscale=True, confidence=0.8)
                if claim_button_location is not None:
                    # Extract coordinates from the located region
                    x, y, _, _ = claim_button_location
                    # Click on the specified coordinates
                    click(x, y)
                    # Set the flag to True to exit the loop
                    claim_button_found = True
                    # Add a delay if needed after clicking the claim button
                    time.sleep(1)
                else:
                    # Optionally add a delay before checking again
                    time.sleep(1)  # Adjust the delay as needed

            except pyautogui.ImageNotFoundException:
                # Handle the case when 'claimcase.png' is not found
                print("Claim case image not found on screen.")
                # Optionally add a delay before checking again
                time.sleep(1)  # Adjust the delay as needed

    else:
        # Handle the case when the initial condition is not met
        print("Case not visible at 490, 550")
        time.sleep(0.5)
