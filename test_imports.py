#!/usr/bin/env python3
"""
Test script to check imports
"""

print("Testing imports...")

try:
    import tkinter as tk
    print("✓ tkinter imported successfully")
except Exception as e:
    print(f"✗ tkinter import failed: {e}")

try:
    from tkinter import ttk, messagebox
    print("✓ tkinter.ttk and messagebox imported successfully")
except Exception as e:
    print(f"✗ tkinter.ttk/messagebox import failed: {e}")

try:
    import sys
    import os
    from pathlib import Path
    print("✓ Standard library imports successful")
except Exception as e:
    print(f"✗ Standard library imports failed: {e}")

# Add src directory to path
try:
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    print("✓ Added src directory to path")
except Exception as e:
    print(f"✗ Failed to add src directory to path: {e}")

try:
    from gui.main_window import MainWindow
    print("✓ MainWindow imported successfully")
except Exception as e:
    print(f"✗ MainWindow import failed: {e}")

try:
    from services.data_manager import DataManager
    print("✓ DataManager imported successfully")
except Exception as e:
    print(f"✗ DataManager import failed: {e}")

print("Import test completed.")