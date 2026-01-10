#!/usr/bin/env python
"""Minimal test to load KV."""
import sys
sys.stdout.flush()

print("Starting import...")
sys.stdout.flush()

try:
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.boxlayout import BoxLayout
    print("Kivy imports OK")
    sys.stdout.flush()
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    import db
    print("db import OK")
    sys.stdout.flush()
except Exception as e:
    print(f"db import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("All imports successful. Loading main...")
sys.stdout.flush()

try:
    from main import KV, RootWidget, PoCApp
    print("main imports OK")
    sys.stdout.flush()
except Exception as e:
    print(f"main import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Test complete - no import errors detected.")
