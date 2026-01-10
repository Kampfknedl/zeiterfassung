#!/usr/bin/env python
"""Debug run to catch exceptions in app startup."""
import traceback
import sys

try:
    print("Loading main.py...")
    from main import PoCApp
    print("App class loaded successfully")
    app = PoCApp()
    print("App instance created")
    app.run()
except Exception as e:
    print(f"CRASH: {e}")
    traceback.print_exc()
    sys.exit(1)
