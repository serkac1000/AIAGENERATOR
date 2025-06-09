"""
MIT App Inventor AIA Generator
Main entry point for the desktop application
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Main application entry point"""
    try:
        # Import GUI after setting up logging
        from gui import AIAGeneratorGUI
        
        # Create and run the application
        root = tk.Tk()
        app = AIAGeneratorGUI(root)
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start the GUI event loop
        root.mainloop()
        
    except ImportError as e:
        messagebox.showerror("Import Error", f"Failed to import required modules: {str(e)}")
        logging.error(f"Import error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        messagebox.showerror("Application Error", f"An unexpected error occurred: {str(e)}")
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
