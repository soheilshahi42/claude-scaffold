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
from rich.box import DOUBLE, HEAVY
from rich.table import Table
from rich.columns import Columns
from rich.padding import Padding
from rich.live import Live

from .icons import icons


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
        
        # Create a centered input prompt
        input_prompt = Text()
        input_prompt.append("▶ ", style=f"bold {self.theme.ORANGE}")
        self.console.print(Align.center(input_prompt), end="")
        
        # Show cursor for input
        print('\033[?25h', end='', flush=True)
        
        # Get input using standard input (questionary doesn't center well)
        if not multiline:
            answer = input(f"") or default
        else:
            # For multiline, still use questionary but with better positioning
            answer = questionary.text(
                "",
                default=default,
                multiline=multiline,
                style=self.qstyle,
                qmark=""
            ).ask()
        
        # Hide cursor again
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
                    return selected
                elif key.lower() == 'y':
                    return True
                elif key.lower() == 'n':
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
        """Show a full-screen progress page with animated loading."""
        import threading
        import time
        
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
        
        def animate():
            nonlocal frame_index, spinner_index
            while self.loading_active:
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
                        # Animate current item
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
                
                # Print layout
                self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
                
                # Update animation indices
                frame_index = (frame_index + 1) % len(loading_frames)
                spinner_index = (spinner_index + 1) % len(spinner_frames)
                
                time.sleep(0.1)
        
        # Start animation in background
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
    
    def stop_progress(self):
        """Stop the progress animation."""
        self.loading_active = False
        if hasattr(self, 'animation_thread'):
            self.animation_thread.join(timeout=0.5)
        
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