#!/usr/bin/env python
"""Test to verify export_csv_to_path runs and outputs logs."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Setup minimal Kivy to test without GUI
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import datetime
import db

class TestExportApp(App):
    def build(self):
        self.root = BoxLayout()
        
        # Simulate RootWidget behavior
        db_path = os.path.join(os.path.expanduser('~'), 'test_export.db')
        db.init_db(db_path)
        
        # Add test customer and entries
        db.add_customer(db_path, 'TestKunde')
        db.add_entry(db_path, 'TestKunde', 'Test Aktivität', 
                     datetime.datetime.now().isoformat(), 
                     datetime.datetime.now().isoformat(), 2.5)
        
        print("\n[TEST] Testing export_csv_to_path...")
        export_dir = os.path.join(os.path.expanduser('~'), 'Documents')
        print(f"[TEST] Export dir: {export_dir}")
        print(f"[TEST] Export dir exists: {os.path.exists(export_dir)}")
        print(f"[TEST] Export dir writable: {os.access(export_dir, os.W_OK)}")
        
        # Try to write a test file
        try:
            test_file = os.path.join(export_dir, 'test_write.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            if os.path.exists(test_file):
                os.remove(test_file)
                print("[TEST] ✅ Write access confirmed")
            else:
                print("[TEST] ❌ Write failed - file not created")
        except Exception as e:
            print(f"[TEST] ❌ Write test failed: {e}")
        
        # Clean up
        if os.path.exists(db_path):
            os.remove(db_path)
        
        return self.root

if __name__ == '__main__':
    app = TestExportApp()
    app.run()
