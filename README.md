
# BEFORE RUNNING THE FILES EXECUTE THE FOLLOWING IN THE TERMINAL FROM THE WORKING FOLDER:
pip install -r requirements.txt

# Key Features:

Multi-line Text Box: The user can type freely in this area.
Timer-Based Text Clearing: If no typing occurs within 5 seconds, the text box is cleared.

Start/Stop Buttons:
Start: Clears the text box and starts monitoring for inactivity.
Stop: Stops the timer and prevents text from being cleared.

# Some Implementation Details:

Disable typing until "Start": The Text widget starts off as DISABLED. It’s only enabled when the "Start" button is pressed.
after() method usage: The after() method is used to check for inactivity and clear the text after 5 seconds. This approach avoids blocking the main thread and keeps the application responsive.
Canceling previous timers: When the user types, the previous after() call is canceled and a new 5-second timer is started.
