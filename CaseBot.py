import customtkinter as ctk
import tkinter as tk
from customtkinter import E, HORIZONTAL, N, NO, NORMAL, ON, S, W, X, Y
from threading import Thread, Event
import time
from claimcase import claim_and_click_gui

class CaseBotApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window size and position
        self.geometry("600x400")  # Adjust the size as needed
        self.title("CaseBot GUI")

        # Entry fields for coordinates
        self.label_x = ctk.CTkLabel(self, text="X Coordinate:")
        self.entry_x = ctk.CTkEntry(self)

        self.label_y = ctk.CTkLabel(self, text="Y Coordinate:")
        self.entry_y = ctk.CTkEntry(self)

        self.label_x.pack(pady=5)
        self.entry_x.pack(pady=5)
        self.label_y.pack(pady=5)
        self.entry_y.pack(pady=5)

        # Slider for confidence
        self.label_confidence = ctk.CTkLabel(self, text="Confidence:")
        self.slider_confidence = ctk.CTkSlider(self, from_=0, to=1, command=self.on_slider_change)

        self.label_confidence.pack(pady=10)
        self.slider_confidence.pack(pady=10)

        # Label to display confidence value
        self.confidence_label = ctk.CTkLabel(self, text="Confidence Value: 0.0")
        self.confidence_label.pack(pady=5)

        # Label to display script status
        self.status_label = ctk.CTkLabel(self, text="Script Status: Stopped")
        self.status_label.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_script)
        self.stop_button = ctk.CTkButton(self, text="Stop", command=self.stop_script, state=NORMAL)

        self.start_button.pack(pady=10)
        self.stop_button.pack(pady=10)

        # Thread variable to store the script thread
        self.script_thread = None
        # Event to signal when to stop the script
        self.stop_event = Event()
        # Event to signal forceful termination
        self.force_stop_event = Event()

    def on_slider_change(self, value):
        confidence = float(value)
        self.confidence_label.configure(text=f"Confidence Value: {confidence}")

    def start_script(self):
        x = int(self.entry_x.get())
        y = int(self.entry_y.get())
        confidence = self.slider_confidence.get()
        print("Script initiated.")

        # Start the script in a new thread
        self.script_thread = Thread(target=self.run_script, args=(x, y, confidence, self.stop_event))
        self.script_thread.start()
        self.status_label.configure(text="Script Status: Running")

    def stop_script(self):
        # Set events to stop the script
        self.stop_event.set()
        self.force_stop_event.set()
        self.status_label.configure(text="Script Status: Stopped")

        if self.script_thread and self.script_thread.is_alive():
            # Wait for the thread to finish with a timeout
            self.script_thread.join(timeout=5)  # Adjust the timeout as needed

    def run_script(self, x, y, confidence, stop_event):
        try:
            while not stop_event.is_set():
                # Call your actual function from claimcase.py
                claim_and_click_gui(x, y, confidence, stop_event)

                # Optionally add a delay before the next iteration
                time.sleep(0.1)  # Adjust the delay as needed

                # Check the force_stop_event and exit the loop if set
                if self.force_stop_event.is_set():
                    print("Force stop initiated.")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Thread exiting.")
            stop_event.set()
            self.force_stop_event.set()

if __name__ == "__main__":
    root = CaseBotApp()
    root.mainloop()
