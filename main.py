"""
Student Management System - Main Entry Point
A desktop application built with Tkinter, applying OOP principles, and using SQLite for database storage.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui import StudentManagementApp
from db import Database

def main():
    """Main function to start the Student Management System"""
    try:
        # Initialize database
        db = Database()
        db.initialize_database()
        
        # Create and run the GUI application
        root = tk.Tk()
        app = StudentManagementApp(root, db)
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
