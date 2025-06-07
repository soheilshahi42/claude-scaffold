"""Retro full-screen UI with Anthropic black and orange theme."""

import os
import shutil
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

import questionary
from questionary import Style as QStyle
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.box import DOUBLE, HEAVY, MINIMAL
from rich.table import Table
from rich.columns import Columns
from rich.padding import Padding
from rich.live import Live

from .icons import icons
from .logger import get_logger


class RetroTheme:
    """Anthropic retro color theme."""
    
    # Anthropic colors
    ORANGE = "#da7756"  # Anthropic orange
    ORANGE_LIGHT = "#e89478"
    ORANGE_DARK = "#bd5d3a"
    
    BLACK = "#000000"
    DARK_GRAY = "#1a1a1a"
    GRAY = "#333333"
    LIGHT_GRAY = "#666666"
    WHITE = "#ffffff"
    
    # Semantic colors
    BACKGROUND = BLACK
    FOREGROUND = ORANGE
    ACCENT = ORANGE_LIGHT
    HIGHLIGHT = ORANGE_DARK
    TEXT = WHITE
    TEXT_DIM = LIGHT_GRAY
    
    # Status colors
    GREEN = "#00ff00"  # Bright green for success
    RED = "#ff0000"    # Bright red for errors
    
    # Retro CRT effect colors
    SCANLINE = "#111111"
    GLOW = ORANGE_DARK


class RetroUI:
    """Full-screen retro UI for Claude Scaffold."""
    
    def __init__(self):
        self.width, self.height = self._get_terminal_size()
        # Create console with reduced height to prevent scrolling
        self.console = Console(height=self.height)
        self.theme = RetroTheme()
        self.logger = get_logger()
        
        # Log UI initialization
        self.logger.debug("RetroUI initialized", {
            "terminal_size": f"{self.width}x{self.height}"
        })
        
        # Questionary style with retro theme
        self.qstyle = QStyle([
            ("qmark", f"fg:{self.theme.ORANGE} bold"),
            ("question", f"fg:{self.theme.WHITE} bold"),
            ("answer", f"fg:{self.theme.ORANGE_LIGHT} bold"),
            ("pointer", f"fg:{self.theme.ORANGE} bold"),
            ("highlighted", f"fg:{self.theme.BLACK} bg:{self.theme.ORANGE}"),
            ("selected", f"fg:{self.theme.ORANGE_LIGHT}"),
            ("separator", f"fg:{self.theme.LIGHT_GRAY}"),
            ("instruction", f"fg:{self.theme.LIGHT_GRAY}"),
            ("text", f"fg:{self.theme.WHITE}"),
            ("disabled", f"fg:{self.theme.GRAY}"),
        ])
        
        # Register cleanup handler
        import atexit
        atexit.register(self.cleanup)
    
    def cleanup(self):
        """Restore terminal state on exit."""
        # Show cursor
        print('\033[?25h', end='', flush=True)
        # Clear screen
        self._clear_screen()
        # Restore cursor
        print('\033[?25h', end='', flush=True)
        
    def _get_terminal_size(self) -> Tuple[int, int]:
        """Get terminal dimensions."""
        size = shutil.get_terminal_size()
        # Reduce height by 1 to prevent scrolling
        return size.columns, size.lines - 1
        
    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
        # Hide cursor to prevent it from appearing below the box
        print('\033[?25l', end='', flush=True)
        
    def _create_header(self, title: str, subtitle: str = "") -> Panel:
        """Create a retro header panel."""
        header_lines = []
        
        # ASCII art logo with glow effect
        logo = Text()
        logo.append("┌─┐┬  ┌─┐┬ ┬┌┬┐┌─┐  ┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┬  ┌┬┐\n", style=f"bold {self.theme.ORANGE}")
        logo.append("│  │  ├─┤│ │ ││├┤   └─┐│  ├─┤├┤ ├┤ │ ││   ││\n", style=f"bold {self.theme.ORANGE_LIGHT}")
        logo.append("└─┘┴─┘┴ ┴└─┘─┴┘└─┘  └─┘└─┘┴ ┴└  └  └─┘┴─┘─┴┘", style=f"bold {self.theme.ORANGE_DARK}")
        
        # Add scanline effect
        logo_with_scanlines = Text()
        for i, line in enumerate(str(logo).split('\n')):
            if i % 2 == 0:
                logo_with_scanlines.append(line + "\n", style=f"on {self.theme.SCANLINE}")
            else:
                logo_with_scanlines.append(line + "\n")
                
        header_lines.append(Align.center(logo_with_scanlines))
        
        if subtitle:
            header_lines.append(Text())
            header_lines.append(Align.center(
                Text(subtitle, style=f"{self.theme.TEXT_DIM} italic")
            ))
            
        # Current section title
        header_lines.append(Text())
        header_lines.append(Align.center(
            Text(f"━━━ {title.upper()} ━━━", style=f"bold {self.theme.ORANGE}")
        ))
        
        return Panel(
            Group(*header_lines),
            border_style=self.theme.ORANGE,
            box=HEAVY,
            padding=(1, 2),
            style=f"on {self.theme.BACKGROUND}"
        )
        
    def _create_content_panel(self, content: Any, title: str = "") -> Panel:
        """Create a content panel with retro styling."""
        return Panel(
            content,
            title=f"[{self.theme.ORANGE}]{'▶ ' + title if title else ''}[/]",
            border_style=self.theme.ORANGE_DARK,
            box=DOUBLE,
            padding=(2, 4),
            style=f"{self.theme.TEXT} on {self.theme.DARK_GRAY}",
            expand=False
        )
        
    def _create_footer(self, hint: str = "") -> Panel:
        """Create a footer with hints."""
        footer_text = Text()
        
        # Navigation hints
        if hint:
            footer_text.append(hint, style=self.theme.TEXT_DIM)
        else:
            footer_text.append("↑↓ Navigate  ", style=self.theme.TEXT_DIM)
            footer_text.append("Enter", style=f"bold {self.theme.ORANGE}")
            footer_text.append(" Select  ", style=self.theme.TEXT_DIM)
            footer_text.append("Ctrl+C", style=f"bold {self.theme.ORANGE}")
            footer_text.append(" Exit", style=self.theme.TEXT_DIM)
            
        # Timestamp
        footer_text.append(f"\n{datetime.now().strftime('%H:%M:%S')}", style=self.theme.GRAY)
        
        return Panel(
            Align.center(footer_text),
            border_style=self.theme.GRAY,
            box=HEAVY,
            style=f"on {self.theme.BACKGROUND}"
        )
        
    def show_welcome_screen(self, project_name: str) -> None:
        """Show the welcome screen."""
        self._clear_screen()
        
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=9),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=3)
        )
        
        # Header
        layout["header"].update(
            self._create_header("INITIALIZING", "Claude Scaffold Project Generator")
        )
        
        # Content
        welcome_text = Text()
        welcome_text.append(f"\n\nProject: ", style=self.theme.TEXT_DIM)
        welcome_text.append(f"{project_name}\n\n", style=f"bold {self.theme.ORANGE}")
        welcome_text.append("▸ Claude AI Enhanced Configuration\n", style=self.theme.ORANGE_LIGHT)
        welcome_text.append("▸ Full-Stack Project Templates\n", style=self.theme.ORANGE_LIGHT)
        welcome_text.append("▸ Test-Driven Development\n", style=self.theme.ORANGE_LIGHT)
        welcome_text.append("▸ Comprehensive Documentation\n\n", style=self.theme.ORANGE_LIGHT)
        
        welcome_text.append("Press ", style=self.theme.TEXT_DIM)
        welcome_text.append("Enter", style=f"bold {self.theme.ORANGE}")
        welcome_text.append(" to begin...", style=self.theme.TEXT_DIM)
        
        layout["content"].update(
            Align.center(
                self._create_content_panel(
                    Align.center(welcome_text, vertical="middle"),
                    "SYSTEM READY"
                ),
                vertical="middle"
            )
        )
        
        # Footer
        layout["footer"].update(self._create_footer("Press Enter to start"))
        
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}", end="")
        # Move cursor to top-left to avoid any extra lines
        print('\033[H', end='', flush=True)
        
        # Wait for Enter without showing cursor
        import sys, tty, termios
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                key = sys.stdin.read(1)
                if key == '\r' or key == '\n':
                    break
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
    def ask_selection(
        self, 
        title: str, 
        question: str, 
        choices: List[Any],
        subtitle: str = "",
        hint: str = ""
    ) -> Any:
        """Show a full-screen selection page with interactive selection."""
        import sys
        import tty
        import termios
        
        # Process choices
        if isinstance(choices[0], dict):
            choice_items = [(c.get("name", str(c)), c.get("value", c)) for c in choices]
        else:
            choice_items = [(str(c), c) for c in choices]
        
        selected_index = 0
        max_visible = 10  # Maximum visible choices
        scroll_offset = 0
        
        while True:
            self._clear_screen()
            
            # Create layout
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=9),
                Layout(name="content", ratio=1),
                Layout(name="footer", size=3)
            )
            
            # Header
            layout["header"].update(
                self._create_header(title, subtitle)
            )
            
            # Content
            content_group = []
            
            # Question
            question_text = Text()
            question_text.append("\n? ", style=f"bold {self.theme.ORANGE}")
            question_text.append(question, style=f"bold {self.theme.WHITE}")
            question_text.append("\n\n")
            content_group.append(Align.center(question_text))
            
            # Calculate visible range
            total_choices = len(choice_items)
            if total_choices > max_visible:
                # Adjust scroll offset to keep selected item visible
                if selected_index < scroll_offset:
                    scroll_offset = selected_index
                elif selected_index >= scroll_offset + max_visible:
                    scroll_offset = selected_index - max_visible + 1
                    
                visible_start = scroll_offset
                visible_end = min(scroll_offset + max_visible, total_choices)
            else:
                visible_start = 0
                visible_end = total_choices
            
            # Show scroll indicator if needed
            if visible_start > 0:
                content_group.append(Align.center(Text("▲ More above ▲", style=self.theme.TEXT_DIM)))
                content_group.append(Text(""))
            
            # Choices
            for i in range(visible_start, visible_end):
                choice_text = Text()
                if i == selected_index:
                    choice_text.append("  ► ", style=f"bold {self.theme.ORANGE}")
                    choice_text.append(choice_items[i][0], style=f"bold {self.theme.WHITE}")
                else:
                    choice_text.append("    ", style="")
                    choice_text.append(choice_items[i][0], style=self.theme.TEXT_DIM)
                content_group.append(Align.center(choice_text))
            
            # Show scroll indicator if needed
            if visible_end < total_choices:
                content_group.append(Text(""))
                content_group.append(Align.center(Text("▼ More below ▼", style=self.theme.TEXT_DIM)))
            
            # Instructions
            content_group.append(Text("\n"))
            instructions = Text()
            instructions.append("↑↓ ", style=f"bold {self.theme.ORANGE}")
            instructions.append("Navigate   ", style=self.theme.TEXT_DIM)
            instructions.append("ENTER ", style=f"bold {self.theme.ORANGE}")
            instructions.append("Select   ", style=self.theme.TEXT_DIM)
            instructions.append("ESC ", style=f"bold {self.theme.ORANGE}")
            instructions.append("Cancel", style=self.theme.TEXT_DIM)
            content_group.append(Align.center(instructions))
            
            content = Panel(
                Align.center(Group(*content_group), vertical="middle"),
                border_style=self.theme.ORANGE_DARK,
                box=DOUBLE,
                padding=(2, 4)
            )
            
            layout["content"].update(
                Align.center(content, vertical="middle")
            )
            
            # Footer
            layout["footer"].update(self._create_footer(hint or "Select an option"))
            
            # Print layout
            self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
            
            # Get single keypress
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
                
                if key == '\r' or key == '\n':  # Enter
                    return choice_items[selected_index][1]
                elif key == '\x1b':  # Escape sequence
                    next_keys = sys.stdin.read(2)
                    if next_keys == '[A':  # Up arrow
                        selected_index = max(0, selected_index - 1)
                    elif next_keys == '[B':  # Down arrow
                        selected_index = min(len(choice_items) - 1, selected_index + 1)
                    elif next_keys == '':  # Just ESC
                        return None
                elif key == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt()
                    
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
    def ask_text(
        self,
        title: str,
        question: str,
        default: str = "",
        subtitle: str = "",
        hint: str = "",
        multiline: bool = False
    ) -> str:
        """Show a full-screen text input page."""
        self._clear_screen()
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=9),
            Layout(name="question", size=4),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=3)
        )
        
        # Header
        layout["header"].update(
            self._create_header(title, subtitle)
        )
        
        # Question
        question_text = Text()
        question_text.append("? ", style=f"bold {self.theme.ORANGE}")
        question_text.append(question, style=f"bold {self.theme.WHITE}")
        layout["question"].update(
            Align.center(
                Panel(
                    Align.center(question_text),
                    border_style=self.theme.ORANGE_DARK,
                    box=DOUBLE,
                    padding=(0, 2)
                )
            )
        )
        
        # Input area preview
        input_panel = Panel(
            Text(f"\n{'(multiline input)' if multiline else '(text input)'}\n", 
                 style=self.theme.TEXT_DIM, justify="center"),
            title=f"[{self.theme.ORANGE}]▶ INPUT[/]",
            border_style=self.theme.ORANGE,
            box=HEAVY,
            padding=(1, 2)
        )
        
        layout["content"].update(
            Align.center(input_panel, vertical="middle")
        )
        
        # Footer
        layout["footer"].update(self._create_footer(hint or "Type your answer"))
        
        # Print layout without newline
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}", end="")
        
        # Clear screen again to prepare for centered input
        self._clear_screen()
        
        # Calculate center position
        term_height = self.height  # Use our adjusted height
        center_y = term_height // 2
        
        # Move to center
        for _ in range(max(0, center_y - 10)):
            self.console.print()
        
        # Create centered question panel
        question_panel = Panel(
            Align.center(question_text),
            border_style=self.theme.ORANGE_DARK,
            box=DOUBLE,
            padding=(1, 4),
            width=80
        )
        self.console.print(Align.center(question_panel))
        self.console.print()
        
        # Show default value if present
        if default:
            default_text = Text(f"Default: {default}", style=self.theme.TEXT_DIM)
            self.console.print(Align.center(default_text))
            self.console.print()
        
        if not multiline:
            # Single line input
            input_prompt = Text()
            input_prompt.append("▶ ", style=f"bold {self.theme.ORANGE}")
            self.console.print(Align.center(input_prompt), end="")
            
            # Show cursor for input
            print('\033[?25h', end='', flush=True)
            
            answer = input(f"") or default
            
            # Hide cursor again
            print('\033[?25l', end='', flush=True)
        else:
            # Multiline input - create a notepad-like text area with input inside the box
            import sys
            import tty
            import termios
            
            # Initialize text buffer  
            lines = []
            current_line = ""
            cursor_pos = 0
            last_was_empty_enter = False  # Track for double enter
            
            # Get terminal dimensions
            term_width, term_height = self._get_terminal_size()
            
            # Calculate box dimensions to fit screen
            box_width = min(term_width - 10, 120)  # Max 120 chars wide, with margins
            box_height = term_height - 15  # Leave room for header and footer
            if box_height < 10:
                box_height = 10  # Minimum height
            elif box_height > 30:
                box_height = 30  # Maximum height
            
            # Center the box horizontally
            start_col = (term_width - box_width - 2) // 2
            if start_col < 2:
                start_col = 2
            
            while True:
                self._clear_screen()
                
                # Create layout with input box
                layout = Layout()
                # Adjust layout sizes based on terminal height
                header_size = 7
                footer_size = 3
                editor_size = term_height - header_size - footer_size - 2
                
                layout.split_column(
                    Layout(name="header", size=header_size),
                    Layout(name="editor", size=editor_size),
                    Layout(name="footer", size=footer_size)
                )
                
                # Header
                header_group = []
                header_group.append(Align.center(Text(title, style=f"bold {self.theme.ORANGE}")))
                header_group.append(Text(""))
                header_group.append(Align.center(question_text))
                
                layout["header"].update(
                    Panel(
                        Group(*header_group),
                        border_style=self.theme.ORANGE_DARK,
                        box=DOUBLE
                    )
                )
                
                # Editor box with current text
                editor_lines = []
                
                # Show default text hint above the box if no input yet
                if default and len(lines) == 0 and current_line == "":
                    editor_lines.append(Text("\n  Current text:", style=self.theme.TEXT_DIM))
                    default_preview = default.split('\n')[0]
                    if len(default_preview) > box_width - 10:
                        default_preview = default_preview[:box_width - 13] + "..."
                    editor_lines.append(Text(f"  {default_preview}", style=self.theme.GRAY))
                    editor_lines.append(Text("  (Press Enter twice to keep, or start typing to replace)\n", style=self.theme.TEXT_DIM))
                
                # Draw the text input box
                editor_lines.append(Text("┌" + "─" * box_width + "┐", style=self.theme.ORANGE))
                
                # Show typed lines
                all_lines = lines + [current_line]
                
                # Calculate what to show (simple scrolling)
                start_line = max(0, len(all_lines) - box_height)
                
                for i in range(box_height):
                    if start_line + i < len(all_lines):
                        line_text = all_lines[start_line + i]
                        # Truncate if too long
                        if len(line_text) > box_width - 2:
                            line_text = line_text[:box_width - 2]
                        # Pad to fill box width
                        line_text = line_text.ljust(box_width - 2)
                        editor_lines.append(Text("│ " + line_text + " │", style=self.theme.ORANGE))
                    else:
                        # Empty line
                        editor_lines.append(Text("│" + " " * box_width + "│", style=self.theme.ORANGE))
                
                editor_lines.append(Text("└" + "─" * box_width + "┘", style=self.theme.ORANGE))
                
                layout["editor"].update(
                    Panel(
                        Group(*editor_lines),
                        title=f"[{self.theme.ORANGE}]▌ TEXT EDITOR ▐[/]",
                        border_style=self.theme.ORANGE,
                        box=HEAVY,
                        padding=(0, 1)
                    )
                )
                
                # Footer
                footer_text = Text()
                footer_text.append("Type your text | ", style=self.theme.TEXT_DIM)
                footer_text.append("ENTER ", style=f"bold {self.theme.ORANGE}")
                footer_text.append("New line | ", style=self.theme.TEXT_DIM)
                footer_text.append("ENTER ENTER ", style=f"bold {self.theme.ORANGE}")
                footer_text.append("Save | ", style=self.theme.TEXT_DIM)
                footer_text.append("ESC ", style=f"bold {self.theme.ORANGE}")
                footer_text.append("Cancel", style=self.theme.TEXT_DIM)
                
                layout["footer"].update(
                    Align.center(footer_text)
                )
                
                # Print layout
                self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
                
                # Position cursor inside the box
                # Calculate where in the editor panel the box starts
                box_start_row = header_size + 2  # Header + border
                if default and len(lines) == 0 and current_line == "":
                    box_start_row += 4  # Add lines for default text preview
                
                # Calculate which line of the box the cursor is on
                current_display_line = len(lines)  # We're always editing the last line
                visible_line = current_display_line - start_line
                
                # Only show cursor if it's in the visible area
                if 0 <= visible_line < box_height:
                    cursor_screen_row = box_start_row + visible_line + 1  # +1 for top border
                    cursor_screen_col = start_col + 2 + cursor_pos  # +2 for border and space
                    
                    # Move cursor to position (account for panel padding)
                    # The panel has padding which shifts content
                    actual_col = start_col + 4 + cursor_pos  # +4 for "│ " and panel padding
                    print(f'\033[{cursor_screen_row};{actual_col}H', end='', flush=True)
                    print('\033[?25h', end='', flush=True)  # Show cursor
                
                # Get single character input
                old_settings = termios.tcgetattr(sys.stdin)
                try:
                    tty.setraw(sys.stdin.fileno())
                    char = sys.stdin.read(1)
                    
                    if char == '\r' or char == '\n':  # Enter
                        if current_line == "" and last_was_empty_enter:
                            # Two consecutive empty enters = done
                            break
                        
                        # Track if this was an empty enter
                        last_was_empty_enter = (current_line == "")
                        
                        # Add line and continue
                        lines.append(current_line)
                        current_line = ""
                        cursor_pos = 0
                    
                    elif char == '\x7f' or char == '\x08':  # Backspace
                        if cursor_pos > 0:
                            current_line = current_line[:cursor_pos-1] + current_line[cursor_pos:]
                            cursor_pos -= 1
                        last_was_empty_enter = False  # Reset on any edit
                    
                    elif char == '\x03':  # Ctrl+C
                        raise KeyboardInterrupt()
                    
                    elif char == '\x1b':  # ESC or arrow keys
                        # Try to peek at next characters without blocking
                        old_settings2 = termios.tcgetattr(sys.stdin)
                        try:
                            # Set non-blocking mode temporarily
                            import fcntl
                            import os
                            flags = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
                            fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, flags | os.O_NONBLOCK)
                            
                            try:
                                next_char = sys.stdin.read(1)
                                if next_char == '[':
                                    arrow = sys.stdin.read(1)
                                    
                                    # We got an arrow key sequence, handle it
                                    if arrow == 'A' or arrow == 'B':  # Up/Down arrows - ignore them
                                        pass  # Do nothing for up/down arrows
                                                
                                    elif arrow == 'D':  # Left arrow
                                        if cursor_pos > 0:
                                            cursor_pos -= 1
                                            
                                    elif arrow == 'C':  # Right arrow
                                        if cursor_pos < len(current_line):
                                            cursor_pos += 1
                                else:
                                    # Not an arrow key sequence, treat as ESC
                                    lines = []
                                    current_line = ""
                                    break
                            except:
                                # No more characters, just ESC
                                lines = []
                                current_line = ""
                                break
                        finally:
                            # Restore blocking mode
                            fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, flags)
                            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings2)
                    
                    elif char >= ' ' and len(current_line) < box_width - 2:  # Printable character
                        current_line = current_line[:cursor_pos] + char + current_line[cursor_pos:]
                        cursor_pos += 1
                        last_was_empty_enter = False  # Reset on any edit
                        
                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            
            # Process final result
            if lines or current_line:
                # Remove trailing empty line if exists
                if current_line:
                    lines.append(current_line)
                while lines and lines[-1] == "":
                    lines.pop()
                answer = '\n'.join(lines) if lines else default
            else:
                answer = default
            
            # Hide cursor
            print('\033[?25l', end='', flush=True)
        
        return answer
        
    def ask_confirm(
        self,
        title: str,
        question: str,
        default: bool = False,
        subtitle: str = "",
        hint: str = ""
    ) -> bool:
        """Show a full-screen confirmation page with interactive selection."""
        import sys
        import tty
        import termios
        
        selected = default  # True = Yes, False = No
        
        while True:
            self._clear_screen()
            
            # Create layout
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=9),
                Layout(name="content", ratio=1),
                Layout(name="footer", size=3)
            )
            
            # Header
            layout["header"].update(
                self._create_header(title, subtitle)
            )
            
            # Content
            confirm_text = Text()
            confirm_text.append("\n\n? ", style=f"bold {self.theme.ORANGE}")
            confirm_text.append(question, style=f"bold {self.theme.WHITE}")
            confirm_text.append("\n\n\n")
            
            # Yes/No options with current selection
            options = Text()
            if selected:
                options.append("    ►  ", style=f"bold {self.theme.ORANGE}")
                options.append("YES", style=f"bold {self.theme.WHITE}")
                options.append("        ", style=self.theme.GRAY)
                options.append("NO", style=self.theme.TEXT_DIM)
            else:
                options.append("       ", style=self.theme.GRAY)
                options.append("YES", style=self.theme.TEXT_DIM)
                options.append("     ►  ", style=f"bold {self.theme.ORANGE}")
                options.append("NO", style=f"bold {self.theme.WHITE}")
            
            options.append("\n\n", style="")
            
            # Instructions
            instructions = Text()
            instructions.append("← → ", style=f"bold {self.theme.ORANGE}")
            instructions.append("Navigate   ", style=self.theme.TEXT_DIM)
            instructions.append("ENTER ", style=f"bold {self.theme.ORANGE}")
            instructions.append("Confirm   ", style=self.theme.TEXT_DIM)
            instructions.append("Y/N ", style=f"bold {self.theme.ORANGE}")
            instructions.append("Quick Select", style=self.theme.TEXT_DIM)
            
            content = Panel(
                Align.center(Group(confirm_text, options, instructions), vertical="middle"),
                border_style=self.theme.ORANGE_DARK,
                box=DOUBLE,
                padding=(2, 4)
            )
            
            layout["content"].update(
                Align.center(content, vertical="middle")
            )
            
            # Footer
            layout["footer"].update(
                self._create_footer(hint or "Select your choice")
            )
            
            # Print layout
            self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
            
            # Get single keypress
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
                
                if key == '\r' or key == '\n':  # Enter
                    # Clear screen before returning
                    self._clear_screen()
                    return selected
                elif key.lower() == 'y':
                    # Clear screen before returning
                    self._clear_screen()
                    return True
                elif key.lower() == 'n':
                    # Clear screen before returning
                    self._clear_screen()
                    return False
                elif key == '\x1b':  # Escape sequence
                    next_key = sys.stdin.read(2)
                    if next_key == '[C':  # Right arrow
                        selected = False
                    elif next_key == '[D':  # Left arrow
                        selected = True
                elif key == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt()
                    
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
    def show_progress(
        self,
        title: str,
        message: str,
        subtitle: str = "",
        items: Optional[List[str]] = None
    ):
        """Show a full-screen progress page with smooth animation."""
        import threading
        import time
        from rich.live import Live
        
        # Animation frames for retro loading
        loading_frames = [
            "█▒▒▒▒▒▒▒▒▒",
            "██▒▒▒▒▒▒▒▒",
            "███▒▒▒▒▒▒▒",
            "████▒▒▒▒▒▒",
            "█████▒▒▒▒▒",
            "██████▒▒▒▒",
            "███████▒▒▒",
            "████████▒▒",
            "█████████▒",
            "██████████",
            "▒█████████",
            "▒▒████████",
            "▒▒▒███████",
            "▒▒▒▒██████",
            "▒▒▒▒▒█████",
            "▒▒▒▒▒▒████",
            "▒▒▒▒▒▒▒███",
            "▒▒▒▒▒▒▒▒██",
            "▒▒▒▒▒▒▒▒▒█",
            "▒▒▒▒▒▒▒▒▒▒",
        ]
        
        # Spinner frames
        spinner_frames = ["◐", "◓", "◑", "◒"]
        
        self.loading_active = True
        frame_index = 0
        spinner_index = 0
        
        def generate_frame():
            nonlocal frame_index, spinner_index
            
            # Create layout
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=9),
                Layout(name="content", ratio=1),
                Layout(name="footer", size=3)
            )
            
            # Header
            layout["header"].update(
                self._create_header(title, subtitle)
            )
            
            # Progress content
            progress_group = []
            
            # Message
            msg_text = Text(f"\n{message}\n", style=f"bold {self.theme.WHITE}")
            progress_group.append(Align.center(msg_text))
            
            # Loading bar
            loading_text = Text()
            loading_text.append("  ", style="")
            loading_text.append(loading_frames[frame_index], style=f"bold {self.theme.ORANGE}")
            loading_text.append("  ", style="")
            progress_group.append(Align.center(loading_text))
            progress_group.append(Text(""))
            
            # Spinner with text
            spinner_text = Text()
            spinner_text.append(spinner_frames[spinner_index], style=f"bold {self.theme.ORANGE}")
            spinner_text.append(" PROCESSING ", style=f"bold {self.theme.WHITE}")
            spinner_text.append(spinner_frames[spinner_index], style=f"bold {self.theme.ORANGE}")
            progress_group.append(Align.center(spinner_text))
            
            # Items if provided
            if items:
                progress_group.append(Text("\n"))
                for i, item in enumerate(items):
                    item_text = Text()
                    # Animate current item (last one)
                    if i == len(items) - 1:
                        item_text.append(f"{spinner_frames[spinner_index]} ", style=f"bold {self.theme.ORANGE}")
                        item_text.append(item, style=f"bold {self.theme.WHITE}")
                    else:
                        item_text.append("✓ ", style=f"bold {self.theme.GREEN}")
                        item_text.append(item, style=self.theme.TEXT_DIM)
                    progress_group.append(Align.center(item_text))
            
            content = Panel(
                Align.center(Group(*progress_group), vertical="middle"),
                title=f"[{self.theme.ORANGE}]◆ PROCESSING ◆[/]",
                border_style=self.theme.ORANGE,
                box=HEAVY,
                padding=(2, 4)
            )
            
            layout["content"].update(
                Align.center(content, vertical="middle")
            )
            
            # Footer
            layout["footer"].update(
                self._create_footer("Please wait...")
            )
            
            # Update indices
            frame_index = (frame_index + 1) % len(loading_frames)
            spinner_index = (spinner_index + 1) % len(spinner_frames)
            
            return layout
        
        # Clear screen once
        self._clear_screen()
        
        # Use Live display to prevent flickering
        self.live_display = Live(
            generate_frame(),
            console=self.console,
            refresh_per_second=10,
            transient=False,
            screen=True  # Use alternate screen buffer
        )
        
        def animate():
            with self.live_display:
                while self.loading_active:
                    self.live_display.update(generate_frame())
                    time.sleep(0.1)
        
        # Start animation in background thread
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
    
    def stop_progress(self):
        """Stop the progress animation."""
        self.loading_active = False
        if hasattr(self, 'animation_thread'):
            self.animation_thread.join(timeout=0.5)
        if hasattr(self, 'live_display'):
            try:
                self.live_display.stop()
            except:
                pass
        # Clear screen after stopping progress
        self._clear_screen()
    
    def ask_feedback(
        self,
        title: str,
        current_value: Any,
        value_type: str = "text",
        subtitle: str = ""
    ) -> Optional[str]:
        """Ask for refinement feedback in retro style."""
        self._clear_screen()
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=9),
            Layout(name="content", ratio=1),
            Layout(name="input", size=8),
            Layout(name="footer", size=3)
        )
        
        # Header
        layout["header"].update(
            self._create_header(title, subtitle)
        )
        
        # Content - show current value
        content_group = []
        content_group.append(Text("\nCurrent suggestion:\n", style=f"bold {self.theme.WHITE}"))
        
        if value_type == "text":
            # Wrap text for better display
            lines = str(current_value).split('\n')
            for line in lines[:10]:  # Show first 10 lines
                if len(line) > 80:
                    line = line[:77] + "..."
                content_group.append(Text(f"  {line}", style=self.theme.ORANGE_LIGHT))
            if len(lines) > 10:
                content_group.append(Text(f"  ... and {len(lines) - 10} more lines", style=self.theme.TEXT_DIM))
        elif value_type == "list":
            for i, item in enumerate(current_value[:5], 1):
                content_group.append(Text(f"  {i}. {str(item)[:80]}", style=self.theme.ORANGE_LIGHT))
            if len(current_value) > 5:
                content_group.append(Text(f"  ... and {len(current_value) - 5} more items", style=self.theme.TEXT_DIM))
        
        content_group.append(Text("\n"))
        content_group.append(Text("Would you like to refine this suggestion?", style=f"bold {self.theme.WHITE}"))
        
        layout["content"].update(
            Panel(
                Align.center(Group(*content_group), vertical="middle"),
                border_style=self.theme.ORANGE_DARK,
                box=DOUBLE,
                padding=(1, 2)
            )
        )
        
        # Input area
        input_text = Text()
        input_text.append("Enter feedback or press ", style=self.theme.TEXT_DIM)
        input_text.append("ENTER", style=f"bold {self.theme.ORANGE}")
        input_text.append(" to accept as-is", style=self.theme.TEXT_DIM)
        
        layout["input"].update(
            Panel(
                Align.center(input_text),
                title=f"[{self.theme.ORANGE}]▌ FEEDBACK ▐[/]",
                border_style=self.theme.ORANGE,
                box=MINIMAL,
                padding=(1, 2)
            )
        )
        
        # Footer
        layout["footer"].update(
            self._create_footer("Type your feedback or press ENTER to skip")
        )
        
        # Print layout
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}", end="")
        
        # Get feedback
        print('\033[?25h', end='', flush=True)  # Show cursor
        feedback = input().strip()
        print('\033[?25l', end='', flush=True)  # Hide cursor
        
        return feedback if feedback else None
        
    def show_results(
        self,
        title: str,
        results: Dict[str, Any],
        subtitle: str = "",
        actions: Optional[List[str]] = None
    ) -> Optional[str]:
        """Show a full-screen results page."""
        self._clear_screen()
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=9),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=3)
        )
        
        # Header
        layout["header"].update(
            self._create_header(title, subtitle)
        )
        
        # Results table
        table = Table(
            show_header=True,
            header_style=f"bold {self.theme.ORANGE}",
            border_style=self.theme.ORANGE_DARK,
            box=HEAVY,
            padding=(0, 1)
        )
        
        table.add_column("Property", style=self.theme.TEXT_DIM)
        table.add_column("Value", style=self.theme.WHITE)
        
        for key, value in results.items():
            table.add_row(key, str(value))
            
        # Actions if provided
        if actions:
            actions_text = Text("\n\nAvailable Actions:\n", style=self.theme.TEXT_DIM)
            for i, action in enumerate(actions, 1):
                actions_text.append(f"\n  [{i}] ", style=self.theme.ORANGE)
                actions_text.append(action, style=self.theme.WHITE)
                
            content = Group(
                Align.center(table),
                Align.center(actions_text)
            )
        else:
            content = Align.center(table)
            
        layout["content"].update(
            Align.center(
                self._create_content_panel(content, "RESULTS"),
                vertical="middle"
            )
        )
        
        # Footer
        layout["footer"].update(
            self._create_footer("Press Enter to continue" if not actions else "Select an action")
        )
        
        # Print layout without newline
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}", end="")
        
        if actions:
            # Get action selection
            choice = input("\nSelect action (number): ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(actions):
                    return actions[idx]
            except ValueError:
                pass
        else:
            # Wait for Enter without showing cursor
            import sys, tty, termios
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                while True:
                    key = sys.stdin.read(1)
                    if key == '\r' or key == '\n':
                        break
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            
        return None
        
    def show_completion(
        self,
        title: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        subtitle: str = ""
    ):
        """Show a full-screen completion page."""
        self._clear_screen()
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=9),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=3)
        )
        
        # Header
        layout["header"].update(
            self._create_header(title, subtitle)
        )
        
        # Success content
        success_text = Text()
        success_text.append("\n✓ ", style=f"bold {self.theme.ORANGE}")
        success_text.append(f"{message}\n\n", style=f"bold {self.theme.WHITE}")
        
        if details:
            for key, value in details.items():
                success_text.append(f"{key}: ", style=self.theme.TEXT_DIM)
                success_text.append(f"{value}\n", style=self.theme.ORANGE_LIGHT)
                
        # ASCII art success indicator
        success_art = Text()
        success_art.append("\n\n╭─────────╮\n", style=self.theme.ORANGE)
        success_art.append("│ SUCCESS │\n", style=f"bold {self.theme.ORANGE}")
        success_art.append("╰─────────╯", style=self.theme.ORANGE)
        
        content = Panel(
            Align.center(
                Group(success_text, success_art),
                vertical="middle"
            ),
            border_style=self.theme.ORANGE,
            box=DOUBLE,
            padding=(2, 4)
        )
        
        layout["content"].update(
            Align.center(content, vertical="middle")
        )
        
        # Footer
        layout["footer"].update(
            self._create_footer("Press Enter to exit")
        )
        
        # Print layout without newline
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}", end="")
        
        # Wait for Enter without showing cursor
        import sys, tty, termios
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                key = sys.stdin.read(1)
                if key == '\r' or key == '\n':
                    break
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)