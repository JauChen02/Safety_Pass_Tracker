#!/usr/bin/env python3
"""
Safety Pass Management System - GUI Application Launcher
Double-click this file to start the application
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox


def check_dependencies():
    """Check if required packages are installed"""
    missing_packages = []

    try:
        import schedule
    except ImportError:
        missing_packages.append('schedule')

    try:
        import pandas
    except ImportError:
        missing_packages.append('pandas')

    return missing_packages


def install_packages(packages):
    """Install missing packages"""
    import subprocess

    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    return True


def main():
    """Main launcher function"""
    print("=" * 60)
    print("🏭 SAFETY PASS MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Starting GUI Application...\n")

    # Check for missing dependencies
    missing = check_dependencies()

    if missing:
        print(f"⚠️  Missing required packages: {', '.join(missing)}")
        print("Installing missing packages automatically...\n")

        if not install_packages(missing):
            print("\n❌ Failed to install required packages.")
            print("Please install manually using: pip install schedule pandas")
            input("\nPress Enter to exit...")
            return

        print("\n✅ All packages installed successfully!")

    try:
        # Import and run the GUI application
        print("🚀 Launching Safety Pass Management System...")
        from safety_pass_gui import main as run_gui
        run_gui()

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\nMake sure all files are in the same folder:")
        print("- run_app.py (this file)")
        print("- safety_pass_gui.py")
        print("- safety_pass_system.py")
        print("- config_example.py")
        input("\nPress Enter to exit...")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

        # Show error in GUI if possible
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Error", f"Failed to start application:\n\n{str(e)}")
        except:
            pass

        input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Critical error: {e}")
        input("Press Enter to exit...")