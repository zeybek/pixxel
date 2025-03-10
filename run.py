#!/usr/bin/env python3
"""
Pixxel - Launcher script
"""
import sys
import os

# Ensure we're in the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.main import main
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all dependencies are installed.")
    sys.exit(1)

if __name__ == "__main__":
    sys.exit(main()) 