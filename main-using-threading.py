import tkinter as tk
import threading
import time

# THIS FILE REFACTORS main.py USING THE PYTHON's THREADING LIBRARY INSTEAD OF THE AFTER METHOD:

# NOTE 1: tkinter not thread safe - handling this:
# 
# Thread-safety: Since tkinter isn't thread-safe, any updates to the GUI (like 
# modifying the Text widget) should only be done in the main thread. We'll use 
# the after() method to update the GUI safely from the worker thread.
#
# Proper thread management: We'll create a background thread that will monitor 
# for user inactivity and clear the text if necessary.

# NOTE 2: Key Points:
#
# Thread-safety: The background thread (created using threading.Thread) monitors 
# the text activity and signals the main thread to clear the text box using 
# self.root.after(0, ...), which safely schedules the text clearing in the main 
# thread.
#
# Locking: A threading.Lock() is used to ensure that the background thread reads 
# and modifies the self.text_modified variable safely when multiple threads are 
# involved.
#
# Thread Lifecycle: The start_timer method creates and starts a new thread to 
# monitor typing inactivity. The stop_timer method sets self.is_running to False 
# to stop the thread.

# NOTE 3: Handling Window Close Event Gracefully:
#
# Non-blocking close: Instead of using thread.join(), we use self.root.after(100, self.check_thread_completion) 
# to check every 100 milliseconds if the background thread is finished. This 
# ensures the main Tkinter loop remains responsive.
#
# Daemon thread: The background thread is set as a daemon thread (self.monitor_thread.daemon = True). 
# This ensures that the thread automatically exits when the main program exits, preventing it from 
# blocking the closure of the app.
#
# Graceful shutdown: When the close button is pressed, self.is_running = False ensures that the 
# background thread stops safely. Instead of immediately blocking with join(), the 
# check_thread_completion method periodically checks if the background thread has finished and 
# then closes the app (self.root.destroy()).
#
# Thread existence check: In the on_closing method, we now check both if the thread 
# (self.monitor_thread) exists and if it is alive. If the thread hasn't been started 
# (i.e., self.monitor_thread is None), the app will close immediately.
#
# Graceful shutdown if thread exists: If the thread exists and is alive, the program 
# will check for thread completion as before. Otherwise, it will immediately call 
# self.root.destroy().




class WriterBlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Writer's Block Alleviator")
        self.text_modified = False
        self.is_running = False
        self.lock = threading.Lock()
        self.monitor_thread = None

        # Handle the close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create a Text widget (multi-line edit box), initially disabled
        self.text_box = tk.Text(root, height=10, width=50, state=tk.DISABLED)
        self.text_box.pack(pady=20)

        # Bind key event to detect typing
        self.text_box.bind("<Key>", self.on_keypress)

        # Create Start and Stop buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side="right", padx=10)

    def on_keypress(self, event):
        # Set a flag when a key is pressed
        with self.lock:
            self.text_modified = True

    def start_timer(self):
        # Clear the text box, enable typing, and start monitoring for inactivity
        self.text_box.config(state=tk.NORMAL)  # Enable text box for typing
        self.text_box.delete(1.0, tk.END)
        self.text_modified = False
        self.is_running = True

        # Start a background thread to monitor typing
        if self.monitor_thread is None or not self.monitor_thread.is_alive():
            self.monitor_thread = threading.Thread(target=self.monitor_typing)
            self.monitor_thread.daemon = True  # Ensure the thread exits with the main program
            self.monitor_thread.start()

    def stop_timer(self):
        # Stop monitoring and disable typing
        self.is_running = False
        self.text_box.config(state=tk.DISABLED)  # Disable text box to prevent further typing

    def monitor_typing(self):
        while self.is_running:
            time.sleep(5)  # Check every 5 seconds
            with self.lock:
                if not self.text_modified:
                    # If no key was pressed within the last 5 seconds, clear the text
                    self.clear_text_in_main_thread()
                self.text_modified = False

    def clear_text_in_main_thread(self):
        # Safely clear text in the main thread using after()
        self.root.after(0, self.clear_text)

    def clear_text(self):
        # Clear the text box
        self.text_box.delete(1.0, tk.END)

    def on_closing(self):
        # Handle the window close event
        self.is_running = False  # Stop the thread safely
        if self.monitor_thread is not None and self.monitor_thread.is_alive():
            self.check_thread_completion()
        else:
            self.root.destroy()  # If the thread was never started or has finished, close the window

    def check_thread_completion(self):
        # Use after() to periodically check if the thread has stopped
        if self.monitor_thread.is_alive():
            self.root.after(100, self.check_thread_completion)
        else:
            self.root.destroy()  # Once the thread is done, close the window

if __name__ == "__main__":
    root = tk.Tk()
    app = WriterBlockApp(root)
    root.mainloop()
