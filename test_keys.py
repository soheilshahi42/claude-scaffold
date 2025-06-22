#!/usr/bin/env python3
"""Test key reading functionality."""

import sys
import os
sys.path.insert(0, 'src')

from claude_scaffold.utils.retro_ui import RetroUI

ui = RetroUI()
print("Press keys to test (Ctrl+C to exit):")
print("Try: Enter, Up Arrow, Down Arrow, ESC")
print("-" * 40)

try:
    while True:
        key = ui._get_key()
        if key:
            if key == '\n':
                print("ENTER pressed")
            elif key == '\x1b':
                print("ESC pressed")
            elif key == '\x03':
                print("Ctrl+C pressed")
                break
            elif key == 'up':
                print("UP ARROW pressed")
            elif key == 'down':
                print("DOWN ARROW pressed")
            else:
                print(f"Key pressed: {repr(key)}")
except KeyboardInterrupt:
    print("\nExiting...")