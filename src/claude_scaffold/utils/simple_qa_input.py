"""Simple Q&A input method without Rich to avoid flicker."""

import signal
import termios
import tty
import sys
import textwrap
from typing import Tuple, List


def simple_qa_input(
    title: str,
    question: str,
    question_number: int,
    category: str,
    allow_skip_after: int = 20,
    subtitle: str = "",
    width: int = 80,
    height: int = 24
) -> Tuple[str, bool]:
    """Simple Q&A input with dynamic text box."""
    
    # ANSI color codes
    ORANGE = "\033[38;5;208m"
    WHITE = "\033[97m"
    DIM = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
    # Track Ctrl+\ press
    ctrl_backslash_pressed = False
    
    def handle_ctrl_backslash(signum, frame):
        nonlocal ctrl_backslash_pressed
        ctrl_backslash_pressed = True
    
    old_handler = signal.signal(signal.SIGQUIT, handle_ctrl_backslash)
    
    # Box dimensions
    box_width = min(70, width - 10)
    inner_width = box_width - 4
    
    def wrap_text(text: str) -> List[str]:
        """Wrap text to fit inside box."""
        if not text:
            return [""]
        return textwrap.wrap(text, width=inner_width) or [""]
    
    def render_screen(text: str, cursor_pos: int):
        """Render the entire screen."""
        # Clear and move to top
        print('\033[2J\033[H', end='')
        
        # Header
        print(f"\n{ORANGE}{'=' * width}{RESET}")
        print(f"{ORANGE}{BOLD}{'CLAUDE SCAFFOLD - Q&A SESSION'.center(width)}{RESET}")
        print(f"{ORANGE}{'=' * width}{RESET}\n")
        
        # Category and question number
        print(f"{DIM}Category:{RESET} {ORANGE}{BOLD}{category.upper()}{RESET}  |  "
              f"{DIM}Question{RESET} {ORANGE}{BOLD}{question_number}{RESET}\n")
        
        # Question
        print(f"{ORANGE}{BOLD}?{RESET} {WHITE}{BOLD}{question}{RESET}\n")
        
        # Skip hint if applicable
        if question_number >= allow_skip_after:
            print(f"{ORANGE}💡{RESET} {DIM}Feeling we have enough info? Press{RESET} "
                  f"{ORANGE}{BOLD}Ctrl+\\{RESET} {DIM}to finish Q&A{RESET}\n")
        
        # Input prompt
        print(f"{ORANGE}📝{RESET} {WHITE}Type your answer below:{RESET}\n")
        
        # Wrap text
        wrapped_lines = wrap_text(text)
        
        # Calculate cursor position in wrapped text
        remaining = cursor_pos
        cursor_line = 0
        cursor_col = 0
        
        for i, line in enumerate(wrapped_lines):
            if remaining <= len(line):
                cursor_line = i
                cursor_col = remaining
                break
            remaining -= len(line)
            if remaining > 0:
                remaining -= 1  # Account for wrapped newline
        
        # Dynamic box height
        min_height = 3
        max_height = 10
        box_height = min(max_height, max(min_height, len(wrapped_lines) + 2))
        
        # Determine visible lines
        visible_start = max(0, cursor_line - (box_height - 3))
        visible_end = min(len(wrapped_lines), visible_start + (box_height - 2))
        
        # Draw box
        print(f"{ORANGE}╭{'─' * box_width}╮{RESET}")
        
        for i in range(box_height - 2):
            line_idx = visible_start + i
            if line_idx < len(wrapped_lines):
                line_text = wrapped_lines[line_idx]
                # Add cursor
                if line_idx == cursor_line:
                    if cursor_col < len(line_text):
                        display = line_text[:cursor_col] + "█" + line_text[cursor_col:]
                    else:
                        display = line_text + "█"
                else:
                    display = line_text
                # Pad to box width
                display = display + " " * (box_width - len(display) - 2)
                print(f"{ORANGE}│{RESET} {display} {ORANGE}│{RESET}")
            else:
                # Empty line with cursor if needed
                if line_idx == cursor_line:
                    print(f"{ORANGE}│{RESET} █{' ' * (box_width - 3)} {ORANGE}│{RESET}")
                else:
                    print(f"{ORANGE}│{RESET} {' ' * box_width} {ORANGE}│{RESET}")
        
        print(f"{ORANGE}╰{'─' * box_width}╯{RESET}")
        
        # Scroll indicators
        if visible_start > 0:
            print(f"{DIM}▲ More above ▲{RESET}")
        if visible_end < len(wrapped_lines):
            print(f"{DIM}▼ More below ▼{RESET}")
        
        # Footer
        print(f"\n{DIM}Type and press{RESET} {ORANGE}{BOLD}ENTER{RESET} {DIM}to submit | {RESET}", end='')
        if question_number >= allow_skip_after:
            print(f"{ORANGE}{BOLD}Ctrl+\\{RESET} {DIM}= Enough info | {RESET}", end='')
        print(f"{ORANGE}{BOLD}Ctrl+C{RESET} {DIM}= Cancel{RESET}")
        
        sys.stdout.flush()
    
    # Hide cursor
    print('\033[?25l', end='', flush=True)
    
    try:
        # Save terminal settings
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        
        # Initialize
        text = ""
        cursor_pos = 0
        
        # Initial render
        render_screen(text, cursor_pos)
        
        while True:
            # Read character
            char = sys.stdin.read(1)
            
            if char == '\r' or char == '\n':  # Enter
                return text, False
            
            elif char == '\x1b':  # Escape sequence
                next_chars = sys.stdin.read(2)
                if next_chars == '[D':  # Left arrow
                    if cursor_pos > 0:
                        cursor_pos -= 1
                        render_screen(text, cursor_pos)
                elif next_chars == '[C':  # Right arrow
                    if cursor_pos < len(text):
                        cursor_pos += 1
                        render_screen(text, cursor_pos)
            
            elif char == '\x7f' or char == '\x08':  # Backspace
                if cursor_pos > 0:
                    text = text[:cursor_pos-1] + text[cursor_pos:]
                    cursor_pos -= 1
                    render_screen(text, cursor_pos)
            
            elif char == '\x1c':  # Ctrl+\
                if ctrl_backslash_pressed and question_number >= allow_skip_after:
                    return "", True
            
            elif char == '\x03':  # Ctrl+C
                raise KeyboardInterrupt()
            
            elif 32 <= ord(char) <= 126:  # Printable
                text = text[:cursor_pos] + char + text[cursor_pos:]
                cursor_pos += 1
                render_screen(text, cursor_pos)
    
    except KeyboardInterrupt:
        raise
    
    finally:
        # Restore
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        signal.signal(signal.SIGQUIT, old_handler)
        print('\033[?25h', end='', flush=True)  # Show cursor
        print('\033[2J\033[H', end='', flush=True)  # Clear screen