import win32api
import win32con
import pyautogui
import time
import pytesseract
import mss
from PIL import Image

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def testclaim_and_click_gui(stop_event, claim_text='Claim Case', completed_text='Completed', claimcase_region=None, completed_region=None, initial_delay=0.5, image_search_delay=1, after_click_delay=0.5, confidence=0.7):
    # Define the regions for 'Claim Case' and 'Completed' text
    claimcase_region = claimcase_region or (275, 453, 663, 972)  # (left, top, right, bottom)
    completed_region = completed_region or (937, 494, 1055, 529)  # (left, top, right, bottom)

    while not stop_event.is_set():  # Check the stop_event before each iteration
        try:
            print("Claim Case Region:", claimcase_region)
            print("Completed Region:", completed_region)
            print("Taking screenshot for 'Claim Case'...")

            # Capture a screenshot of the specified region for 'Claim Case' text using mss
            with mss.mss() as sct:
                # Get the details of all available monitors
                monitors = sct.monitors
                # Select the monitor based on the specified index
                monitor = monitors[2]  # Change the index if needed
                # Define the region of interest on the selected monitor
                monitor_region = {
                    "left": monitor["left"] + claimcase_region[0],
                    "top": monitor["top"] + claimcase_region[1],
                    "width": claimcase_region[2] - claimcase_region[0],
                    "height": claimcase_region[3] - claimcase_region[1]
                }
                # Capture the screenshot of the specified region
                claimcase_screenshot = sct.grab(monitor_region)

            # Convert the screenshot to a format compatible with pytesseract
            claimcase_img = Image.frombytes("RGB", claimcase_screenshot.size, claimcase_screenshot.rgb)

            # Perform OCR processing for 'Claim Case' text
            claimcase_text = pytesseract.image_to_string(claimcase_img)
            print("OCR processing for 'Claim Case'...")
            print("Extracted text for 'Claim Case':", claimcase_text)

            # Check if "Claim Case" text is found
            if claim_text in claimcase_text:
                print(f"Found '{claim_text}' text on the screen.")
                print(f"Extracted text for 'Claim Case': {claimcase_text}")
                # Extract coordinates of the 'Claim Case' text
                x, y = pyautogui.locateCenterOnScreen('claimcase.png', confidence=confidence, region=claimcase_region)
                print(f"Clicking at coordinates ({x}, {y}) for '{claim_text}' text.")
                # Click on the specified coordinates
                click(x, y)
                # Add a delay if needed after clicking the claim button
                time.sleep(after_click_delay)
                continue  # Continue searching for the claim button after claiming

            print("Taking screenshot for 'Completed'...")

            # Capture a screenshot of the specified region for 'Completed' text using mss
            with mss.mss() as sct:
                # Get the details of all available monitors
                monitors = sct.monitors
                # Select the monitor based on the specified index
                monitor = monitors[2]  # Change the index if needed
                # Define the region of interest on the selected monitor
                monitor_region = {
                    "left": monitor["left"] + completed_region[0],
                    "top": monitor["top"] + completed_region[1],
                    "width": completed_region[2] - completed_region[0],
                    "height": completed_region[3] - completed_region[1]
                }
                # Capture the screenshot of the specified region
                completed_screenshot = sct.grab(monitor_region)

            # Convert the screenshot to a format compatible with pytesseract
            completed_img = Image.frombytes("RGB", completed_screenshot.size, completed_screenshot.rgb)

            # Perform OCR processing for 'Completed' text
            completed_text = pytesseract.image_to_string(completed_img)
            print("OCR processing for 'Completed'...")
            print("Extracted text for 'Completed':", completed_text)

            # Check if "Completed" text is found
            if completed_text in completed_text:
                print("Found 'Completed' text on the screen.")
                print(f"Extracted text for 'Completed': {completed_text}")
                # Extract coordinates of the 'Completed' text
                x, y = pyautogui.locateCenterOnScreen('completed.png', confidence=confidence, region=completed_region)
                print(f"Clicking at coordinates ({x}, {y}) for 'Completed' text.")
                # Click on the specified coordinates
                click(x, y)
                # Add a delay if needed after clicking the completed button
                time.sleep(after_click_delay)
                continue  # Continue searching for the claim button after claiming

        except Exception as e:
            print(f"Error occurred: {str(e)}")

        # Optionally add a delay before checking again
        time.sleep(image_search_delay)
