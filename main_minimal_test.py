#!/usr/bin/env python
"""MINIMAL test APK - just show a label to verify Kivy basics work on Android"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import os
import sys

class TestApp(App):
    def build(self):
        print("[MINIMAL TEST] build() called")
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text='Zeiterfassung - Android Test', size_hint_y=0.2, font_size='20sp', bold=True)
        root.add_widget(title)
        
        status = Label(
            text='✓ Kivy loads successfully\n✓ No database queries\n✓ No PDF generation\n✓ Just widgets',
            size_hint_y=0.6
        )
        root.add_widget(status)
        
        close_btn = Button(text='Close App', size_hint_y=0.2)
        close_btn.bind(on_release=lambda *args: App.get_running_app().stop())
        root.add_widget(close_btn)
        
        print("[MINIMAL TEST] UI built successfully")
        return root
    
    def on_start(self):
        print("[MINIMAL TEST] on_start() called")

if __name__ == '__main__':
    print("[MINIMAL TEST] App starting...")
    try:
        app = TestApp()
        print("[MINIMAL TEST] App instance created")
        app.run()
        print("[MINIMAL TEST] App finished")
    except Exception as e:
        print(f"[MINIMAL TEST ERROR] {e}")
        import traceback
        traceback.print_exc()
