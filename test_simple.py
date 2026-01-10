#!/usr/bin/env python
"""Minimal test with immediate flush."""
import sys
import os

# Force unbuffered
os.environ['PYTHONUNBUFFERED'] = '1'

print("1. Testing print...", flush=True)

try:
    print("2. Testing import kivy...", flush=True)
    from kivy.app import App
    print("3. Kivy loaded", flush=True)
except Exception as e:
    print(f"ERROR in kivy import: {e}", flush=True)
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)

try:
    print("4. Testing import db...", flush=True)
    import db
    print("5. db loaded", flush=True)
except Exception as e:
    print(f"ERROR in db import: {e}", flush=True)
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)

print("All imports OK!", flush=True)
input("Press Enter to exit...")
