import mss

def capture_screens():
    with mss.mss() as sct:
        # Get information about available monitors
        monitors = sct.monitors

        # Iterate over each monitor
        for i, monitor in enumerate(monitors):
            print(f"Monitor {i + 1}:")
            print("    Position:", monitor["left"], monitor["top"])
            print("    Resolution:", monitor["width"], "x", monitor["height"])
            
            # Screenshot the current monitor
            monitor_img = sct.grab(monitor)

            # Save or process the screenshot as needed
            output_file = f"monitor_{i + 1}.png"
            mss.tools.to_png(monitor_img.rgb, monitor_img.size, output=output_file)
            print(f"    Screenshot saved as '{output_file}'")

if __name__ == "__main__":
    capture_screens()
