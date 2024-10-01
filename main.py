import tkinter as tk

class WriterBlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Writer's Block Alleviator")
        self.text_modified = False
        self.is_running = False
        self.timer_id = None

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
        self.text_modified = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)  # Cancel the previous timer
        self.timer_id = self.root.after(5000, self.clear_text)  # Set a new 5 second timer

    def start_timer(self):
        # Clear the text box, enable typing, and reset the timer
        self.text_box.config(state=tk.NORMAL)  # Enable text box for typing
        self.text_box.delete(1.0, tk.END)
        self.text_modified = False
        self.is_running = True

        # Set a 5 second delay for the first time, just in case no key is pressed
        self.timer_id = self.root.after(5000, self.clear_text)

    def stop_timer(self):
        # Stop the timer and disable typing
        self.is_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)  # Cancel the active timer
        self.text_box.config(state=tk.DISABLED)  # Disable text box to prevent further typing

    def clear_text(self):
        # Clear the text if no typing for 5 seconds
        if self.is_running:
            self.text_box.delete(1.0, tk.END)
            self.text_modified = False

if __name__ == "__main__":
    root = tk.Tk()
    app = WriterBlockApp(root)
    root.mainloop()
