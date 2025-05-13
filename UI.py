import Model
import tkinter as tk
from tkinter import simpledialog, messagebox

from Model import evaluarEcuación


def display_message_window(message):
    """Displays a message in a simple tkinter window."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    messagebox.showinfo("hell nah", message)

def get_input_window():
    """Opens a simple dialog to get input from the user."""
    root = tk.Tk()
    root.withdraw()

    user_input = "(10 + cos(2)) * 3"

    if user_input is not None:
        display_message_window(evaluarEcuación(user_input) )

if __name__ == "__main__":

    # Example 2: Get input from the user and display it
    get_input_window()