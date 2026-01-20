#!/usr/bin/env python
"""Minimal test to identify Android crash point"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import os
import datetime
import sys
import traceback

# Crash logger for Android debugging
def _install_crash_logger():
    def _hook(exc_type, exc, tb):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lines = [
            f"[{timestamp}] Uncaught exception in test app",
            ''.join(traceback.format_exception(exc_type, exc, tb)),
        ]
        candidates = [
            '/sdcard/Documents/Zeiterfassung/crash.txt',
            os.path.join(os.path.expanduser('~'), 'Documents', 'Zeiterfassung', 'crash.txt'),
        ]
        for path in candidates:
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'a', encoding='utf-8') as f:
                    f.write('\n'.join(lines) + '\n')
                break
            except Exception:
                pass
    sys.excepthook = _hook

_install_crash_logger()

KV = '''
#:kivy 2.0

<TestWidget>:
    orientation: 'vertical'
    padding: 10
    spacing: 10
    
    Label:
        text: 'Zeiterfassung Android Test'
        size_hint_y: 0.2
        font_size: '24sp'
        bold: True
    
    Label:
        text: 'If you see this, basic KV loading works!'
        size_hint_y: 0.3
    
    Label:
        text: 'Test Point 1: KV loaded'
        size_hint_y: 0.2
    
    Label:
        text: 'Test Point 2: BoxLayout created'
        size_hint_y: 0.2
    
    Label:
        text: 'Test Point 3: All working'
        size_hint_y: 0.1
'''

class TestWidget(BoxLayout):
    pass

class TestApp(App):
    def build(self):
        print('[ANDROID TEST] build() called')
        Builder.load_string(KV)
        print('[ANDROID TEST] KV loaded')
        root = TestWidget()
        print('[ANDROID TEST] TestWidget created')
        return root

if __name__ == '__main__':
    print('[ANDROID TEST] App starting')
    app = TestApp()
    print('[ANDROID TEST] App created, about to run()')
    app.run()
    print('[ANDROID TEST] App finished')
