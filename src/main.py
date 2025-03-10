#!/usr/bin/env python3
"""
Pixxel - A simple Pixel Art conversion tool
"""
import os
import sys
from pathlib import Path
import tkinter as tk

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.app_window import AppWindow
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running the application from the correct directory.")
    sys.exit(1)

def main():
    """Initialize and run the application"""
    try:
        root = tk.Tk()
        root.title("Pixxel")
        app = AppWindow(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main()) 