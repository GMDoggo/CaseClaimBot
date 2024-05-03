import win32api
import win32con
import pyautogui
import time

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def claim_and_click_gui(x_entry, y_entry, confidence_entry, stop_event, claim_button_images=['claimcase.png'], grayscale=True, initial_delay=0.5, image_search_delay=1, after_click_delay=0.5):
    # Convert entry values to integers
    x, y = int(x_entry), int(y_entry)
    confidence = float(confidence_entry)

    # Reset the flag variable for each iteration of the outer loop
    claim_button_found = False

    while not stop_event.is_set():  # Check the stop_event before each iteration
        # Check for the exact color at (x, y)
        pixel_color = pyautogui.pixel(x, y)
        if pixel_color == (26, 30, 40):
            # If case is visible, click it
            time.sleep(10)
            click(x, y)
            # Give enough time for the tab to load
            time.sleep(5)

            for claim_button_image in claim_button_images:
                try:
                    # Look for the claimcase images on screen
                    claim_button_location = pyautogui.locateOnScreen(claim_button_image, grayscale=grayscale, confidence=confidence)
                    if claim_button_location is not None:
                        # Extract coordinates from the located region
                        claim_x, claim_y, _, _ = claim_button_location
                        # Click on the specified coordinates
                        click(claim_x, claim_y)
                        # Set the flag to True to exit the loop
                        claim_button_found = True
                        # Add a delay if needed after clicking the claim button
                        time.sleep(after_click_delay)
                        break  # Exit the loop once a claim button is found
                    else:
                        # Optionally add a delay before checking again
                        time.sleep(image_search_delay)  # Adjust the delay as needed

                except pyautogui.ImageNotFoundException:
                    # Handle the case when none of the claimcase images are found
                    print(f"Claim case image '{claim_button_image}' not found on screen.")
                    # Optionally add a delay before checking again
                    time.sleep(0.25)  # Adjust the delay as needed

        else:
            # Handle the case when the initial condition is not met
            time.sleep(initial_delay)
