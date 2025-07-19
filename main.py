"""
Habit Tracker GUI Application
Main entry point for the Pixela-based habit tracker
"""

import tkinter as tk
from main_window import HabitTrackerApp

def main():
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()