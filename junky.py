import mss
from PIL import Image, ImageDraw
import pytesseract

# Define the monitor index you want to capture (monitor #3)
monitor_index = 2

# Define claimcase_region using top-left and bottom-right corner coordinates
claimcase_region = (937, 494, 1055, 529)  # (left, top, right, bottom)

# Unpack the region tuple into variables
left, top, right, bottom = claimcase_region

# Print the values
print("Left coordinate:", left)
print("Top coordinate:", top)
print("Right coordinate:", right)
print("Bottom coordinate:", bottom)

# Capture a screenshot of the specified region for 'Claim Case' text using mss
with mss.mss() as sct:
    # Get the details of all available monitors
    monitors = sct.monitors
    # Select the monitor based on the specified index
    monitor = monitors[monitor_index]
    # Define the region of interest on the selected monitor
    monitor_region = {
        "left": monitor["left"] + left,
        "top": monitor["top"] + top,
        "width": right - left,
        "height": bottom - top
    }
    # Capture the screenshot of the specified region
    claimcase_screenshot = sct.grab(monitor_region)

# Convert the screenshot to a format compatible with PIL
claimcase_img = Image.frombytes("RGB", claimcase_screenshot.size, claimcase_screenshot.rgb)

# Draw a rectangle around the searched area
draw = ImageDraw.Draw(claimcase_img)
draw.rectangle([left, top, right, bottom], outline="red")

# Perform OCR processing for 'Claim Case' text
claimcase_text = pytesseract.image_to_string(claimcase_img)
print("OCR processing for 'Claim Case'...")
print("Extracted text for 'Claim Case':", claimcase_text)

# Show the image with the highlighted region
claimcase_img.show()
