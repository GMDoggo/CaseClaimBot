import customtkinter as ctk
import tkinter as tk
from customtkinter import E, N, NO, NORMAL, ON, S, W, X, Y
from threading import Thread, Event
import time
from test import testclaim_and_click_gui
from claimcase import claim_and_click_gui

class HomeScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SOC Bot Scripts")  # Set a bold title

        # Create a label for the title with increased font size
        title_label = ctk.CTkLabel(self, text="SOC Bot Scripts", font=ctk.CTkFont(size=40, weight="bold"))
        title_label.pack(pady=20)

        # Create a dropdown menu with script options
        self.script_options = ["CaseBotApp", "TestCaseBotApp"]  # Add more scripts as needed
        self.script_var = ctk.StringVar(self)
        self.script_var.set(self.script_options[0])  # Default script

        # Increase the size of the dropdown menu
        self.script_dropdown = ctk.CTkOptionMenu(self, values=self.script_options, variable=self.script_var, font=ctk.CTkFont(size=20))
        self.script_dropdown.pack(pady=30)

        # Button to launch the selected script with increased size
        self.launch_button = ctk.CTkButton(self, text="Launch Script", command=self.launch_script, font=ctk.CTkFont(size=20))
        self.launch_button.pack(pady=20)

        # Set the selected app instance to None initially
        self.selected_app = None

    def launch_script(self):
        selected_script = self.script_var.get()

        if selected_script == "CaseBotApp":
            # Hide the HomeScreen
            self.withdraw()

            # Launch CaseBotApp GUI
            self.selected_app = CaseBotApp(self)
            self.selected_app.protocol("WM_DELETE_WINDOW", self.on_closing_selected_app)  # Bind the closing event
            self.selected_app.mainloop()

        elif selected_script == "TestCaseBotApp":
            # Hide the HomeScreen
            self.withdraw()

            # Launch TestCaseBotApp GUI
            self.selected_app = TestCaseBotApp(self)
            self.selected_app.protocol("WM_DELETE_WINDOW", self.on_closing_selected_app)  # Bind the closing event
            self.selected_app.mainloop()

    def on_closing_selected_app(self):
        # Destroy the selected app window
        self.selected_app.destroy()

        # Show the HomeScreen when the selected app is closed
        self.deiconify()

    def on_closing(self):
        # Destroy the current window
        self.destroy()

        # If there's an open selected app, destroy it
        if self.selected_app:
            self.selected_app.destroy()




class CaseBotApp(ctk.CTk):
    def __init__(self, home_screen, on_close_callback=None):
        super().__init__()

        # Store the callback function
        self.on_close_callback = on_close_callback
        # Store the reference to the HomeScreen instance
        self.home_screen = home_screen

        # Set window size and position
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
        self.force_stop_event = None  # Initialize force_stop_event as None initially

    def on_slider_change(self, value):
        confidence = float(value)
        self.confidence_label.configure(text=f"Confidence Value: {confidence}")

    def start_script(self):
        if self.script_thread and self.script_thread.is_alive():
            # If a thread is already running, don't start a new one
            print("Script is already running.")
            return

        # Create a new instance of force_stop_event each time you start the script
        self.force_stop_event = Event()
        x = int(self.entry_x.get())
        y = int(self.entry_y.get())
        confidence = self.slider_confidence.get()
        print("Script initiated.")

        # Clear stop_event before starting a new thread
        self.stop_event.clear()

        # Start the script in a new thread
        self.script_thread = Thread(target=self.run_script, args=(x, y, confidence, self.stop_event))
        self.script_thread.start()
        self.status_label.configure(text="Script Status: Running")

    def stop_script(self):
        # Set events to stop the script
        self.stop_event.set()
        if self.force_stop_event:
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
                if self.force_stop_event and self.force_stop_event.is_set():
                    print("Force stop initiated.")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Thread exiting.")
            stop_event.set()
            if self.force_stop_event:
                self.force_stop_event.set()

    def on_closing(self):
        # Check if the application has already been destroyed
        if not self.winfo_exists():
            return

        # Destroy the current window
        self.destroy()

        # Show the HomeScreen when CaseBotApp is closed
        self.home_screen.deiconify()

class TestCaseBotApp(ctk.CTk):
    def __init__(self, home_screen):
        super().__init__()

        # Store the reference to the HomeScreen instance
        self.home_screen = home_screen

        # Set window title
        self.title("CaseBot GUI")

        # Label to display script status
        self.status_label = ctk.CTkLabel(self, text="Script Status: Stopped")
        self.status_label.pack(pady=10)

        # Button to start the script
        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_script)
        self.start_button.pack(pady=10)

        # Button to stop the script
        self.stop_button = ctk.CTkButton(self, text="Stop", command=self.stop_script, state=ctk.NORMAL)
        self.stop_button.pack(pady=10)

        # Thread variable to store the script thread
        self.script_thread = None

        # Event to signal when to stop the script
        self.stop_event = Event()

    def start_script(self):
        if self.script_thread and self.script_thread.is_alive():
            print("Script is already running.")
            return

        print("Script initiated.")
        self.stop_event.clear()  # Clear stop_event before starting a new thread

        # Start the script in a new thread
        self.script_thread = Thread(target=self.run_script)
        self.script_thread.start()
        self.status_label.configure(text="Script Status: Running")

    def stop_script(self):
        self.stop_event.set()  # Set event to stop the script
        self.status_label.configure(text="Script Status: Stopped")

    def run_script(self):
        try:
            while not self.stop_event.is_set():
                # Call claim_and_click_gui function from test.py
                testclaim_and_click_gui(self.stop_event)

                # Optionally add a delay before the next iteration
                time.sleep(0.1)  # Adjust the delay as needed

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            print("Thread exiting.")
            self.stop_event.set()

    def on_closing(self):
        if not self.winfo_exists():
            return

        self.destroy()
        self.home_screen.deiconify()

if __name__ == "__main__":
    home_screen = HomeScreen()
    home_screen.mainloop()