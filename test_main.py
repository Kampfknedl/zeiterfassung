#!/usr/bin/env python
"""Test main.py loading."""
import sys
import os

os.environ['PYTHONUNBUFFERED'] = '1'

print("1. Testing import main...", flush=True)

try:
    import main
    print("2. main loaded successfully", flush=True)
except Exception as e:
    print(f"ERROR in main import: {e}", flush=True)
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)

print("3. Creating app instance...", flush=True)

try:
    app = main.PoCApp()
    print("4. App instance created", flush=True)
except Exception as e:
    print(f"ERROR creating app: {e}", flush=True)
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)

print("5. Running app...", flush=True)
try:
    app.run()
except Exception as e:
    print(f"ERROR running app: {e}", flush=True)
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)
