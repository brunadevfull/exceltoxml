#!/usr/bin/env python3
"""
Conversor Excel → XML - Sistema Banco do Brasil
Aplicação desktop para converter planilhas Excel em arquivos XML
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path
import traceback

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("Starting Excel to XML Converter...")

try:
    from gui.main_window import MainWindow
    from services.data_manager import DataManager
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    traceback.print_exc()
    exit(1)

class ConversorApp:
    def __init__(self):
        print("Initializing application...")
        try:
            self.root = tk.Tk()
            self.root.title("Conversor Excel → XML - Sistema BB v2.0")
            self.root.geometry("1400x900")
            self.root.minsize(1200, 700)
            print("✓ Tkinter window created")
            
            # Initialize data manager
            self.data_manager = DataManager()
            print("✓ Data manager initialized")
            
            # Initialize main window
            self.main_window = MainWindow(self.root, self.data_manager)
            print("✓ Main window initialized")
            
            # Configure window icon and properties
            self.root.configure(bg='#f0f0f0')
            
            # Center window on screen
            self.center_window()
            print("✓ Window centered")
            
            print("Application initialization complete!")
            
        except Exception as e:
            print(f"✗ Initialization failed: {e}")
            traceback.print_exc()
            raise
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def run(self):
        """Run the application"""
        print("Starting main loop...")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Application interrupted by user")
        except Exception as e:
            print(f"✗ Runtime error: {e}")
            traceback.print_exc()
            try:
                messagebox.showerror("Erro Fatal", f"Erro inesperado: {str(e)}")
            except:
                pass
            
if __name__ == "__main__":
    try:
        app = ConversorApp()
        app.run()
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        traceback.print_exc()
