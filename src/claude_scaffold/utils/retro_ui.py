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
            # Single line input with better layout
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
            
            # Content - combine question and input in one panel
            content_group = []
            
            # Question
            question_text = Text()
            question_text.append("\n? ", style=f"bold {self.theme.ORANGE}")
            question_text.append(question, style=f"bold {self.theme.WHITE}")
            question_text.append("\n\n")
            content_group.append(Align.center(question_text))
            
            # Input prompt
            input_text = Text()
            input_text.append("Type your answer below:\n\n", style=self.theme.TEXT_DIM)
            content_group.append(Align.center(input_text))
            
            # Show default if present
            if default:
                default_text = Text()
                default_text.append("Default: ", style=self.theme.TEXT_DIM)
                default_text.append(default, style=self.theme.ORANGE_LIGHT)
                default_text.append("\n\n", style="")
                content_group.append(Align.center(default_text))
            
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
            layout["footer"].update(
                self._create_footer(hint or "Type your answer and press ENTER")
            )
            
            # Print layout
            self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
            
            # Get input at bottom
            print('\033[?25h', end='', flush=True)  # Show cursor
            answer = input("\n> ") or default
            print('\033[?25l', end='', flush=True)  # Hide cursor
        else:
            # Multiline input - first ask user which mode they prefer
            mode = self.ask_selection(
                "INPUT MODE",
                "How would you like to enter your text?",
                [
                    {"name": "📝 Simple editor (recommended for short texts)", "value": "simple"},
                    {"name": "📋 Paste mode (for large texts from external editor)", "value": "paste"},
                    {"name": "↩️ Keep default text", "value": "default"}
                ],
                subtitle=title,
                hint="Choose your preferred input method"
            )
            
            if mode == "default":
                return default
            elif mode == "simple":
                # Use questionary with multiline support
                self._clear_screen()
                
                # Show header
                print(f"\n\033[38;2;218;119;86m{'═' * 80}\033[0m")
                print(f"\033[38;2;218;119;86m{title.center(80)}\033[0m")
                print(f"\033[38;2;218;119;86m{'═' * 80}\033[0m\n")
                
                # Show current text if any
                if default:
                    print("Current text:")
                    print(f"\033[38;2;102;102;102m{default[:200]}{'...' if len(default) > 200 else ''}\033[0m\n")
                
                print(f"✏️  {question}")
                print("(Press Tab to toggle between single/multi-line mode)\n")
                
                # Use questionary for input with arrow key support
                import questionary
                answer = questionary.text(
                    "",
                    default=default,
                    multiline=True,
                    style=self.qstyle
                ).ask()
                
                if answer is None:  # User cancelled
                    answer = default
                    
                return answer
                
            else:  # paste mode
                self._clear_screen()
                
                # Show instructions
                layout = Layout()
                layout.split_column(
                    Layout(name="header", size=7),
                    Layout(name="instructions", size=12),
                    Layout(name="footer", size=3)
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
                
                # Instructions
                instr_lines = []
                instr_lines.append(Text("\n  📋 PASTE MODE", style=f"bold {self.theme.ORANGE}"))
                instr_lines.append(Text("  " + "─" * 60, style=self.theme.ORANGE_DARK))
                
                if default:
                    instr_lines.append(Text("\n  Current text preview:", style=self.theme.TEXT_DIM))
                    preview = default[:150] + "..." if len(default) > 150 else default
                    instr_lines.append(Text(f"  {preview.split(chr(10))[0][:70]}", style=self.theme.GRAY))
                
                instr_lines.append(Text("\n  📌 Instructions:", style=f"bold {self.theme.ORANGE}"))
                instr_lines.append(Text("     1. Paste your entire text below", style=self.theme.WHITE))
                instr_lines.append(Text("     2. Press Ctrl+D when done", style=self.theme.WHITE))
                instr_lines.append(Text("     3. Press Ctrl+C to cancel", style=self.theme.WHITE))
                
                layout["instructions"].update(
                    Panel(
                        Group(*instr_lines),
                        border_style=self.theme.ORANGE,
                        box=HEAVY,
                        padding=(1, 2)
                    )
                )
                
                # Footer
                footer_text = Text()
                footer_text.append("Paste your text below | ", style=self.theme.TEXT_DIM)
                footer_text.append("Ctrl+D ", style=f"bold {self.theme.ORANGE}")
                footer_text.append("Save | ", style=self.theme.TEXT_DIM)
                footer_text.append("Ctrl+C ", style=f"bold {self.theme.ORANGE}")
                footer_text.append("Cancel", style=self.theme.TEXT_DIM)
                
                layout["footer"].update(
                    Align.center(footer_text)
                )
                
                # Print layout
                self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
                
                # Simple input collection
                print(f"\n\033[38;2;218;119;86m{'─' * 80}\033[0m\n")
                print('\033[?25h', end='', flush=True)  # Show cursor
                
                try:
                    lines = []
                    print("📋 Paste your text now (press Ctrl+D when done):\n")
                    
                    try:
                        while True:
                            line = input()
                            lines.append(line)
                    except EOFError:
                        pass
                
                    # Join all lines
                    entered_text = '\n'.join(lines) if lines else ""
                    
                    if entered_text:
                        # Show review screen
                        self._clear_screen()
                        
                        # Create review layout
                        review_layout = Layout()
                        review_layout.split_column(
                            Layout(name="header", size=5),
                            Layout(name="content", ratio=1),
                            Layout(name="footer", size=5)
                        )
                        
                        # Header
                        review_layout["header"].update(
                            Panel(
                                Align.center(Text("REVIEW YOUR TEXT", style=f"bold {self.theme.ORANGE}")),
                                border_style=self.theme.ORANGE_DARK,
                                box=DOUBLE
                            )
                        )
                        
                        # Content - show the text in a scrollable view
                        text_lines = entered_text.split('\n')
                        content_lines = []
                        content_lines.append(Text(f"\n  Total lines: {len(text_lines)}", style=self.theme.ORANGE))
                        content_lines.append(Text(f"  Total characters: {len(entered_text)}\n", style=self.theme.ORANGE))
                        content_lines.append(Text("  Preview (first 30 lines):", style=self.theme.TEXT_DIM))
                        content_lines.append(Text("  " + "─" * 80, style=self.theme.ORANGE_DARK))
                        
                        # Show first 30 lines
                        for i, line in enumerate(text_lines[:30]):
                            if len(line) > 100:
                                line = line[:97] + "..."
                            content_lines.append(Text(f"  {line}", style=self.theme.WHITE))
                        
                        if len(text_lines) > 30:
                            content_lines.append(Text(f"\n  ... and {len(text_lines) - 30} more lines", style=self.theme.TEXT_DIM))
                        
                        review_layout["content"].update(
                            Panel(
                                Group(*content_lines),
                                border_style=self.theme.ORANGE,
                                box=MINIMAL,
                                padding=(1, 2)
                            )
                        )
                        
                        # Footer
                        confirm = self.ask_confirm(
                            "CONFIRM TEXT",
                            "Use this text?",
                            default=True,
                            subtitle="Review complete"
                        )
                        
                        if confirm:
                            answer = entered_text
                        else:
                            answer = default
                    else:
                        answer = default
                        
                except KeyboardInterrupt:
                    # Ctrl+C pressed, use default
                    answer = default
                    
                # Hide cursor
                print('\033[?25l', end='', flush=True)
        
        return answer
    
    def show_enhancement_options(self, project_description: str) -> str:
        """Show special enhancement options screen with rich UX."""
        import sys
        import tty
        import termios
        
        selected = 2  # Default to option 2 (Enhance with Claude)
        
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
                self._create_header("ENHANCEMENT OPTIONS", "Choose how to proceed with your project")
            )
            
            # Content - Options
            content_group = []
            
            # Project description (truncated if too long)
            desc_text = Text()
            desc_text.append("\n? ", style=f"bold {self.theme.ORANGE}")
            desc_text.append("Project: ", style=f"bold {self.theme.WHITE}")
            
            # Take only first line and truncate if needed
            first_line = project_description.split('\n')[0].strip()
            max_desc_length = 80
            if len(first_line) > max_desc_length:
                truncated_desc = first_line[:max_desc_length-3] + "..."
            else:
                truncated_desc = first_line
            
            desc_text.append(truncated_desc, style=self.theme.ORANGE_LIGHT)
            desc_text.append("\n\n")
            content_group.append(Align.center(desc_text))
            
            # Options
            options = [
                {
                    "num": "1",
                    "title": "CONTINUE AS IS",
                    "desc": "Use your original description\nwithout any modifications",
                    "hint": "Simple projects with clear requirements"
                },
                {
                    "num": "2", 
                    "title": "ENHANCE WITH CLAUDE",
                    "desc": "Let Claude analyze and improve\nyour project specification",
                    "hint": "Get professional structure & best practices"
                },
                {
                    "num": "3",
                    "title": "Q&A DEEP DIVE ✨",
                    "desc": "Interactive Q&A session with Claude\n(20-100 questions) for detailed planning",
                    "hint": "Complex projects needing detailed specs"
                }
            ]
            
            # Show options with selection
            for i, opt in enumerate(options, 1):
                option_text = Text()
                
                if i == selected:
                    option_text.append("\n  ► ", style=f"bold {self.theme.ORANGE}")
                    option_text.append(f"{opt['num']}. {opt['title']}", style=f"bold {self.theme.WHITE}")
                    option_text.append("\n     ", style="")
                    option_text.append(opt['desc'].replace('\n', '\n     '), style=self.theme.ORANGE_LIGHT)
                    option_text.append("\n     ", style="")
                    option_text.append(f"[{opt['hint']}]", style=self.theme.TEXT_DIM)
                else:
                    option_text.append("\n    ", style="")
                    option_text.append(f"{opt['num']}. {opt['title']}", style=self.theme.TEXT_DIM)
                    option_text.append("\n     ", style="")
                    option_text.append(opt['desc'].replace('\n', '\n     '), style=self.theme.GRAY)
                
                content_group.append(Align.center(option_text))
            
            # Special note for Q&A mode
            content_group.append(Text("\n"))
            note_text = Text()
            note_text.append("Note: ", style=f"bold {self.theme.ORANGE}")
            note_text.append("Q&A mode allows you to press ", style=self.theme.TEXT_DIM)
            note_text.append("Ctrl+\\", style=f"bold {self.theme.ORANGE}")
            note_text.append(" when you have enough information", style=self.theme.TEXT_DIM)
            content_group.append(Align.center(note_text))
            
            # Instructions
            content_group.append(Text("\n"))
            instructions = Text()
            instructions.append("↑↓ ", style=f"bold {self.theme.ORANGE}")
            instructions.append("Navigate   ", style=self.theme.TEXT_DIM)
            instructions.append("ENTER ", style=f"bold {self.theme.ORANGE}")
            instructions.append("Select   ", style=self.theme.TEXT_DIM)
            instructions.append("1-3 ", style=f"bold {self.theme.ORANGE}")
            instructions.append("Quick Select", style=self.theme.TEXT_DIM)
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
            layout["footer"].update(self._create_footer("Select your enhancement option"))
            
            # Print layout
            self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
            
            # Get input
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
                
                if key == '\r' or key == '\n':  # Enter
                    return str(selected)
                elif key in ['1', '2', '3']:  # Direct number selection
                    return key
                elif key == '\x1b':  # Escape sequence
                    next_keys = sys.stdin.read(2)
                    if next_keys == '[A':  # Up arrow
                        selected = max(1, selected - 1)
                    elif next_keys == '[B':  # Down arrow
                        selected = min(3, selected + 1)
                elif key == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt()
                    
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
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
            
            # Truncate long messages to prevent overflow
            display_message = message
            if '\n' in message:
                # For multiline messages, take only the first line
                display_message = message.split('\n')[0].strip()
            
            # Further truncate if still too long
            max_msg_length = 60
            if len(display_message) > max_msg_length:
                display_message = display_message[:max_msg_length-3] + "..."
            
            # Message
            msg_text = Text(f"\n{display_message}\n", style=f"bold {self.theme.WHITE}")
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
                # Limit items shown to prevent overflow
                visible_items = items[-5:] if len(items) > 5 else items
                for i, item in enumerate(visible_items):
                    item_text = Text()
                    # Truncate long items
                    display_item = item[:50] + "..." if len(item) > 50 else item
                    
                    # Animate current item (last one)
                    if i == len(visible_items) - 1:
                        item_text.append(f"{spinner_frames[spinner_index]} ", style=f"bold {self.theme.ORANGE}")
                        item_text.append(display_item, style=f"bold {self.theme.WHITE}")
                    else:
                        item_text.append("✓ ", style=f"bold {self.theme.GREEN}")
                        item_text.append(display_item, style=self.theme.TEXT_DIM)
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
        # Always clear screen and reset console state
        self._clear_screen()
        # Ensure console is in a good state
        self.console.clear()
        print('\033[?25h', end='', flush=True)  # Show cursor
    
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
        elif value_type == "dict":
            for i, (key, value) in enumerate(list(current_value.items())[:5], 1):
                content_group.append(Text(f"  {i}. {key}: {str(value)[:60]}", style=self.theme.ORANGE_LIGHT))
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
    
    def show_paginated_results(
        self,
        title: str,
        results: Dict[str, Any],
        subtitle: str = "",
        items_per_page: int = 8
    ) -> None:
        """Show results with pagination for large datasets."""
        import sys
        import tty
        import termios
        
        items = list(results.items())
        total_items = len(items)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        current_page = 0
        
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
            page_subtitle = f"{subtitle} - Page {current_page + 1} of {total_pages}"
            layout["header"].update(
                self._create_header(title, page_subtitle)
            )
            
            # Get items for current page
            start_idx = current_page * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)
            page_items = items[start_idx:end_idx]
            
            # Results table for current page
            table = Table(
                show_header=True,
                header_style=f"bold {self.theme.ORANGE}",
                border_style=self.theme.ORANGE_DARK,
                box=HEAVY,
                padding=(0, 1)
            )
            
            # Dynamically adjust column widths based on content
            max_key_length = max(len(str(key)) for key, _ in page_items) if page_items else 20
            key_width = min(max_key_length + 2, 30)
            
            table.add_column("Property", style=self.theme.TEXT_DIM, width=key_width, no_wrap=True)
            table.add_column("Value", style=self.theme.WHITE, overflow="fold", max_width=self.width - key_width - 20)
            
            for key, value in page_items:
                value_str = str(value)
                # For very long content, show a preview with option to expand
                if len(value_str) > 500:
                    # Show first 400 chars with indication there's more
                    lines = value_str[:400].split('\n')
                    preview = '\n'.join(lines[:10])  # Max 10 lines
                    if len(value_str) > 400 or len(lines) > 10:
                        preview += f"\n\n[... {len(value_str) - len(preview)} more characters ...]"
                    table.add_row(key, preview)
                else:
                    table.add_row(key, value_str)
            
            # Navigation info
            nav_text = Text()
            nav_text.append(f"\n\nShowing items {start_idx + 1}-{end_idx} of {total_items}", 
                           style=self.theme.TEXT_DIM)
            
            if total_pages > 1:
                nav_text.append("\n\n")
                if current_page > 0:
                    nav_text.append("◀ PREV ", style=f"bold {self.theme.ORANGE}")
                else:
                    nav_text.append("◀ PREV ", style=self.theme.GRAY)
                    
                nav_text.append("| ", style=self.theme.TEXT_DIM)
                
                if current_page < total_pages - 1:
                    nav_text.append("NEXT ▶", style=f"bold {self.theme.ORANGE}")
                else:
                    nav_text.append("NEXT ▶", style=self.theme.GRAY)
                    
                nav_text.append(" | ", style=self.theme.TEXT_DIM)
                nav_text.append("ENTER ", style=f"bold {self.theme.ORANGE}")
                nav_text.append("Continue", style=self.theme.WHITE)
            else:
                nav_text.append("\n\nPress ")
                nav_text.append("ENTER ", style=f"bold {self.theme.ORANGE}")
                nav_text.append("to continue", style=self.theme.WHITE)
            
            content = Group(
                Align.center(table),
                Align.center(nav_text)
            )
            
            layout["content"].update(
                Align.center(
                    self._create_content_panel(content, "RESULTS"),
                    vertical="middle"
                )
            )
            
            # Footer
            if total_pages > 1:
                footer_hint = "◀ ▶ Navigate pages | ENTER Continue"
            else:
                footer_hint = "Press ENTER to continue"
                
            layout["footer"].update(
                self._create_footer(footer_hint)
            )
            
            # Print layout
            self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
            
            # Get input
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
                
                if key == '\r' or key == '\n':  # Enter - continue
                    break
                elif key == '\x1b':  # Arrow keys
                    next_keys = sys.stdin.read(2)
                    if next_keys == '[D' and current_page > 0:  # Left arrow - previous page
                        current_page -= 1
                    elif next_keys == '[C' and current_page < total_pages - 1:  # Right arrow - next page
                        current_page += 1
                elif key == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt()
                    
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
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
    
    def ask_qa_input(
        self,
        title: str,
        question: str,
        question_number: int,
        category: str,
        allow_skip_after: int = 1,
        subtitle: str = ""
    ) -> Tuple[str, bool]:
        """Q&A input with dynamic resizing text box that wraps and grows/shrinks.
        
        Returns:
            Tuple of (answer, enough_signal) where enough_signal is True if user pressed Ctrl+\
        """
        import termios
        import tty
        import textwrap
        import sys
        
        # We'll handle Ctrl+\ directly as a character, no need for signal handler
        
        # Initialize text buffer
        text = ""
        cursor_pos = 0
        box_width = min(70, self.width - 20)
        inner_width = box_width - 4  # Account for borders and padding
        
        # Fixed box dimensions
        min_box_height = 3
        max_box_height = 10
        
        def wrap_text(text: str) -> List[str]:
            """Wrap text to fit inside box."""
            if not text:
                return [""]
            return textwrap.wrap(text, width=inner_width) or [""]
        
        # Hide cursor during rendering
        print('\033[?25l', end='', flush=True)
        
        try:
            # Clear screen first
            self._clear_screen()
            
            # Draw static layout first (header, question, footer)
            # Create layout
            layout = Layout()
            
            # Calculate dynamic sizes
            question_area_size = max(8, (self.height - 20 - max_box_height) // 2)
            input_area_size = self.height - 9 - question_area_size - 3
            
            layout.split_column(
                Layout(name="header", size=9),
                Layout(name="question", size=question_area_size),
                Layout(name="input_area", size=input_area_size),
                Layout(name="footer", size=3)
            )
            
            # Header
            layout["header"].update(
                self._create_header(title, subtitle)
            )
            
            # Question panel
            question_group = []
            cat_text = Text()
            cat_text.append(f"Category: ", style=self.theme.TEXT_DIM)
            cat_text.append(category.upper(), style=f"bold {self.theme.ORANGE}")
            cat_text.append(f"  |  Question ", style=self.theme.TEXT_DIM)
            cat_text.append(str(question_number), style=f"bold {self.theme.ORANGE}")
            question_group.append(Align.center(cat_text))
            question_group.append(Text())
            
            q_text = Text()
            q_text.append("? ", style=f"bold {self.theme.ORANGE}")
            wrapped_q = textwrap.fill(question, width=min(100, self.width - 20))
            q_text.append(wrapped_q, style=f"bold {self.theme.WHITE}")
            question_group.append(Align.center(q_text))
            
            layout["question"].update(
                Panel(
                    Align.center(Group(*question_group), vertical="middle"),
                    border_style=self.theme.ORANGE_DARK,
                    box=DOUBLE,
                    padding=(1, 4),
                    expand=True
                )
            )
            
            # Input area placeholder
            input_group = []
            
            if question_number >= allow_skip_after:
                skip_text = Text()
                skip_text.append("💡 ", style=f"bold {self.theme.ORANGE}")
                skip_text.append("Feeling we have enough info? Press ", style=self.theme.TEXT_DIM)
                skip_text.append("Ctrl+D", style=f"bold {self.theme.ORANGE}")
                skip_text.append(" or ", style=self.theme.TEXT_DIM)
                skip_text.append("ESC ESC", style=f"bold {self.theme.ORANGE}")
                skip_text.append(" to finish Q&A", style=self.theme.TEXT_DIM)
                input_group.append(Align.center(skip_text))
                input_group.append(Text())
            
            input_text = Text()
            input_text.append("📝 ", style=f"bold {self.theme.ORANGE}")
            input_text.append("Type your answer below:", style=self.theme.WHITE)
            input_group.append(Align.center(input_text))
            input_group.append(Text())
            
            # Add placeholder for box
            for _ in range(max_box_height):
                input_group.append(Text())
            
            layout["input_area"].update(
                Panel(
                    Group(*input_group),
                    title=f"[{self.theme.ORANGE}]▶ YOUR ANSWER[/]",
                    border_style=self.theme.ORANGE,
                    box=HEAVY,
                    padding=(1, 2),
                    expand=True
                )
            )
            
            # Footer
            footer_text = Text()
            footer_text.append("Type and press ", style=self.theme.TEXT_DIM)
            footer_text.append("ENTER", style=f"bold {self.theme.ORANGE}")
            footer_text.append(" to submit | ", style=self.theme.TEXT_DIM)
            if question_number >= allow_skip_after:
                footer_text.append("Ctrl+D", style=f"bold {self.theme.ORANGE}")
                footer_text.append(" = Enough info | ", style=self.theme.TEXT_DIM)
            footer_text.append("Ctrl+C", style=f"bold {self.theme.ORANGE}")
            footer_text.append(" = Cancel", style=self.theme.TEXT_DIM)
            
            layout["footer"].update(self._create_footer(""))
            
            # Print static layout
            self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
            
            # Calculate box position on screen
            # Header (9) + question area + spacing in input panel
            box_start_row = 9 + question_area_size + 5
            if question_number >= allow_skip_after:
                box_start_row += 2
            
            # Center the box horizontally
            box_left_col = (self.width - box_width) // 2
            
            # Get terminal settings
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
            
            # Initial render
            wrapped_lines = wrap_text(text)
            cursor_line = 0
            cursor_col = 0
            
            def render_box():
                """Render just the input box at its position."""
                # Calculate box height
                content_height = max(1, len(wrapped_lines))
                box_height = min(max_box_height, max(min_box_height, content_height + 2))
                
                # Save cursor position
                print('\033[s', end='', flush=True)
                
                # Move to box position
                print(f'\033[{box_start_row};{box_left_col}H', end='', flush=True)
                
                # Draw box
                # Top border
                print(f"\033[38;2;218;119;86m╭{'─' * box_width}╮\033[0m", flush=True)
                
                # Content lines
                visible_start = max(0, cursor_line - (box_height - 3))
                visible_end = min(len(wrapped_lines), visible_start + (box_height - 2))
                
                for i in range(box_height - 2):
                    line_idx = visible_start + i
                    print(f'\033[{box_start_row + i + 1};{box_left_col}H', end='', flush=True)
                    
                    if line_idx < len(wrapped_lines):
                        line_text = wrapped_lines[line_idx]
                        # Show cursor on current line
                        if line_idx == cursor_line:
                            if cursor_col < len(line_text):
                                display_line = line_text[:cursor_col] + "█" + line_text[cursor_col:]
                            else:
                                display_line = line_text + "█"
                        else:
                            display_line = line_text
                        
                        # Pad line to box width
                        padding_needed = box_width - len(display_line) - 2
                        display_text = f"{display_line}{' ' * padding_needed}"
                        print(f"\033[38;2;218;119;86m│ \033[0m{display_text}\033[38;2;218;119;86m │\033[0m", flush=True)
                    else:
                        # Empty line
                        if line_idx == cursor_line:
                            print(f"\033[38;2;218;119;86m│ \033[0m█{' ' * (box_width - 2)}\033[38;2;218;119;86m │\033[0m", flush=True)
                        else:
                            print(f"\033[38;2;218;119;86m│{' ' * (box_width + 2)}│\033[0m", flush=True)
                
                # Clear any extra lines below the box
                for i in range(box_height - 2, max_box_height - 2):
                    print(f'\033[{box_start_row + i + 1};{box_left_col}H', end='', flush=True)
                    print(' ' * (box_width + 4), flush=True)
                
                # Bottom border
                print(f'\033[{box_start_row + box_height - 1};{box_left_col}H', end='', flush=True)
                print(f"\033[38;2;218;119;86m╰{'─' * box_width}╯\033[0m", flush=True)
                
                # Restore cursor position
                print('\033[u', end='', flush=True)
            
            # Initial box render
            render_box()
            
            while True:
                # Read single character
                char = sys.stdin.read(1)
                
                if char == '\r' or char == '\n':  # Enter - submit
                    return text, False
                
                elif char == '\x1b':  # Escape sequence
                    next_chars = sys.stdin.read(2)
                    if next_chars == '[D':  # Left arrow
                        if cursor_pos > 0:
                            cursor_pos -= 1
                    elif next_chars == '[C':  # Right arrow
                        if cursor_pos < len(text):
                            cursor_pos += 1
                    elif next_chars == '[A':  # Up arrow
                        # Move up a line
                        if cursor_line > 0:
                            cursor_line -= 1
                            # Adjust cursor position
                            line_start = sum(len(wrapped_lines[i]) + 1 for i in range(cursor_line))
                            cursor_pos = min(line_start + cursor_col, len(text))
                    elif next_chars == '[B':  # Down arrow
                        # Move down a line
                        if cursor_line < len(wrapped_lines) - 1:
                            cursor_line += 1
                            # Adjust cursor position
                            line_start = sum(len(wrapped_lines[i]) + 1 for i in range(cursor_line))
                            cursor_pos = min(line_start + cursor_col, len(text))
                    elif next_chars == '\x1b':  # ESC ESC - double escape to skip
                        if question_number >= allow_skip_after:
                            return "", True
                
                elif char == '\x7f' or char == '\x08':  # Backspace
                    if cursor_pos > 0:
                        text = text[:cursor_pos-1] + text[cursor_pos:]
                        cursor_pos -= 1
                
                elif char == '\x04':  # Ctrl+D - alternative skip key
                    if question_number >= allow_skip_after:
                        return "", True
                
                elif char == '\x1c':  # Ctrl+\ 
                    if question_number >= allow_skip_after:
                        return "", True
                
                elif char == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt()
                
                elif 32 <= ord(char) <= 126:  # Printable characters
                    text = text[:cursor_pos] + char + text[cursor_pos:]
                    cursor_pos += 1
                
                # Re-wrap text and update cursor position
                wrapped_lines = wrap_text(text)
                
                # Calculate cursor line and column from cursor position
                remaining_pos = cursor_pos
                cursor_line = 0
                cursor_col = 0
                
                for i, line in enumerate(wrapped_lines):
                    if remaining_pos <= len(line):
                        cursor_line = i
                        cursor_col = remaining_pos
                        break
                    remaining_pos -= len(line)
                    # Account for implicit newline between wrapped lines
                    if remaining_pos > 0:
                        remaining_pos -= 1
                
                # Always re-render the box
                render_box()
                
        except KeyboardInterrupt:
            raise
            
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            print('\033[?25h', end='', flush=True)  # Show cursor
    
    def show_specification_sections(self, title: str, sections: Dict[str, str], subtitle: str = "") -> None:
        """Show specification sections in a more readable format."""
        import textwrap
        
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
        
        # Content - show sections as formatted text
        content_lines = []
        
        for section_title, section_content in sections.items():
            # Section title
            title_text = Text()
            title_text.append(f"\n▶ {section_title.upper()}", style=f"bold {self.theme.ORANGE}")
            content_lines.append(title_text)
            content_lines.append(Text("─" * 60, style=self.theme.ORANGE_DARK))
            
            # Section content - wrap long lines
            wrapped_content = textwrap.fill(section_content, width=80, break_long_words=False)
            content_text = Text(wrapped_content, style=self.theme.WHITE)
            content_lines.append(content_text)
        
        # Create scrollable view
        content_group = Group(*content_lines)
        
        layout["content"].update(
            Panel(
                content_group,
                title=f"[{self.theme.ORANGE}]▶ DETAILS[/]",
                border_style=self.theme.ORANGE,
                box=HEAVY,
                padding=(1, 2),
                expand=True
            )
        )
        
        # Footer
        layout["footer"].update(
            self._create_footer("Press ENTER to continue")
        )
        
        # Print layout
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
        
        # Wait for Enter
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
    
    def show_qa_progress(self, message: str = "Generating next question...", duration: float = 0):
        """Show a progress screen while generating Q&A questions.
        
        Args:
            message: The message to display
            duration: If > 0, show animated progress for this many seconds
        """
        import threading
        import time
        from rich.live import Live
        
        # Clear screen and immediately show static progress
        self._clear_screen()
        
        # Create static progress layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=9),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=3)
        )
        
        # Header
        layout["header"].update(
            self._create_header("Q&A SESSION", "Claude is thinking...")
        )
        
        # Progress content
        progress_group = []
        
        # Message
        msg_text = Text(f"\n{message}\n", style=f"bold {self.theme.WHITE}")
        progress_group.append(Align.center(msg_text))
        
        # Static Claude art
        claude_art = Text()
        claude_art.append("\n     🤖\n", style=f"bold {self.theme.ORANGE}")
        claude_art.append("    /│\\\n", style=self.theme.ORANGE_LIGHT)
        claude_art.append("   / │ \\\n", style=self.theme.ORANGE_LIGHT)
        progress_group.append(Align.center(claude_art))
        
        # Loading animation
        loading_text = Text()
        loading_text.append("\n◆ ◇ ◆ ◇ ◆ ◇ ◆\n", style=f"bold {self.theme.ORANGE}")
        progress_group.append(Align.center(loading_text))
        
        # Status
        status_text = Text()
        status_text.append("\nAnalyzing previous answers...\n", style=self.theme.TEXT_DIM)
        status_text.append("Formulating contextual question...\n", style=self.theme.TEXT_DIM)
        progress_group.append(Align.center(status_text))
        
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
        
        # Show the static progress immediately
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}", height=self.height)
        
        # Only animate if duration > 0
        if duration > 0:
            self.loading_active = True
            frame_index = 0
            
            loading_frames = ["◆ ◇ ◆ ◇ ◆ ◇ ◆", "◇ ◆ ◇ ◆ ◇ ◆ ◇", "◆ ◇ ◆ ◇ ◆ ◇ ◆", "◇ ◆ ◇ ◆ ◇ ◆ ◇"]
            robot_frames = ["🤖", "🤖", "🤖", "🤖"]
            
            def generate_frame():
                nonlocal frame_index
                
                # Reuse the same layout structure but update animations
                progress_group = []
                
                # Message
                msg_text = Text(f"\n{message}\n", style=f"bold {self.theme.WHITE}")
                progress_group.append(Align.center(msg_text))
                
                # Animated Claude thinking
                claude_art = Text()
                claude_art.append(f"\n     {robot_frames[frame_index % len(robot_frames)]}\n", style=f"bold {self.theme.ORANGE}")
                claude_art.append("    /│\\\n", style=self.theme.ORANGE_LIGHT)
                claude_art.append("   / │ \\\n", style=self.theme.ORANGE_LIGHT)
                progress_group.append(Align.center(claude_art))
                
                # Loading animation
                loading_text = Text()
                loading_text.append(f"\n{loading_frames[frame_index % len(loading_frames)]}\n", style=f"bold {self.theme.ORANGE}")
                progress_group.append(Align.center(loading_text))
                
                # Status
                status_text = Text()
                status_text.append("\nAnalyzing previous answers...\n", style=self.theme.TEXT_DIM)
                status_text.append("Formulating contextual question...\n", style=self.theme.TEXT_DIM)
                progress_group.append(Align.center(status_text))
                
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
                
                frame_index += 1
                return layout
            
            # Animate with lower refresh rate
            def animate():
                end_time = time.time() + duration
                while self.loading_active and time.time() < end_time:
                    # Move cursor to home and update
                    print('\033[H', end='', flush=True)
                    self.console.print(generate_frame(), style=f"on {self.theme.BACKGROUND}", height=self.height)
                    time.sleep(0.5)  # Lower refresh rate
            
            # Start animation in background
            self.animation_thread = threading.Thread(target=animate, daemon=True)
            self.animation_thread.start()
    
    def stop_qa_progress(self):
        """Stop the Q&A progress animation if running."""
        if hasattr(self, 'loading_active'):
            self.loading_active = False
        if hasattr(self, 'animation_thread'):
            self.animation_thread.join(timeout=0.5)
        # Clear screen to prepare for next display
        self._clear_screen()