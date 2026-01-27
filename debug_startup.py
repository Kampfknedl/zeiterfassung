#!/usr/bin/env python3
"""
Minimal Android test - checks if basic imports and App startup works
"""
import sys
import os
import traceback

print("\n" + "="*50)
print("ZEITERFASSUNG - STARTUP DEBUG")
print("="*50 + "\n")

# Step 1: Import Kivy
print("[1/5] Importing Kivy...")
try:
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.boxlayout import BoxLayout
    print("      [OK] Kivy imported")
except Exception as e:
    print(f"      [FAIL] {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 2: Import db module
print("[2/5] Importing db module...")
try:
    import db
    print("      [OK] db module imported")
except Exception as e:
    print(f"      [FAIL] {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 3: Import main components
print("[3/5] Importing main components...")
try:
    from main import RootWidget, KV, _install_crash_logger
    print("      [OK] main components imported")
except Exception as e:
    print(f"      [FAIL] {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 4: Load KV
print("[4/5] Loading KV layout...")
try:
    Builder.load_string(KV)
    print("      [OK] KV loaded")
except Exception as e:
    print(f"      [FAIL] {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 5: Create RootWidget
print("[5/5] Creating RootWidget...")
try:
    root = RootWidget()
    print("      [OK] RootWidget created")
except Exception as e:
    print(f"      [FAIL] {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*50)
print("[SUCCESS] ALL CHECKS PASSED - App should start!")
print("="*50 + "\n")
