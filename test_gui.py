#!/usr/bin/env python3
"""
Test script to check GUI initialization
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("Testing GUI initialization...")

# Test 1: Basic tkinter window
try:
    print("Creating basic tkinter window...")
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("400x300")
    
    label = tk.Label(root, text="Test Label")
    label.pack(pady=20)
    
    print("✓ Basic tkinter window created")
    
    # Test if we can update the window
    root.update()
    print("✓ Window update successful")
    
    root.destroy()
    print("✓ Window destroyed successfully")
    
except Exception as e:
    print(f"✗ Basic tkinter test failed: {e}")
    exit(1)

# Test 2: Data manager initialization
try:
    print("Testing DataManager initialization...")
    from services.data_manager import DataManager
    data_manager = DataManager()
    print("✓ DataManager created successfully")
    
    # Test getting responsibles
    responsibles = data_manager.get_responsibles()
    print(f"✓ Found {len(responsibles)} responsibles")
    
except Exception as e:
    print(f"✗ DataManager test failed: {e}")
    exit(1)

# Test 3: Main window initialization  
try:
    print("Testing MainWindow initialization...")
    from gui.main_window import MainWindow
    
    root = tk.Tk()
    root.title("Test MainWindow")
    root.geometry("1400x900")
    
    main_window = MainWindow(root, data_manager)
    print("✓ MainWindow created successfully")
    
    root.update()
    print("✓ MainWindow update successful")
    
    root.destroy()
    print("✓ MainWindow destroyed successfully")
    
except Exception as e:
    print(f"✗ MainWindow test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("All GUI tests passed!")