"""Cross-platform getch implementation."""

import os
import sys


class Getch:
    """Gets a single character from standard input."""
    
    def __init__(self):
        self.impl = _GetchWindows() if os.name == 'nt' else _GetchUnix()
    
    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __call__(self):
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            # Handle escape sequences for arrow keys
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A':
                        return 'UP'
                    elif ch3 == 'B':
                        return 'DOWN'
                    elif ch3 == 'C':
                        return 'RIGHT'
                    elif ch3 == 'D':
                        return 'LEFT'
                # ESC key
                return 'ESC'
            elif ch == '\r':
                return 'ENTER'
            elif ch == '\x03':
                raise KeyboardInterrupt()
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class _GetchWindows:
    def __call__(self):
        import msvcrt
        ch = msvcrt.getch()
        if ch in [b'\xe0', b'\x00']:  # Special keys
            ch2 = msvcrt.getch()
            if ch2 == b'H':
                return 'UP'
            elif ch2 == b'P':
                return 'DOWN'
            elif ch2 == b'K':
                return 'LEFT'
            elif ch2 == b'M':
                return 'RIGHT'
        elif ch == b'\x1b':
            return 'ESC'
        elif ch == b'\r':
            return 'ENTER'
        elif ch == b'\x03':
            raise KeyboardInterrupt()
        return ch.decode('utf-8', errors='ignore')


getch = Getch()