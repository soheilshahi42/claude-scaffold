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
            # Single line input with Claude Code CLI-style box
            self._clear_screen()
            
            # Create layout for input
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=9),
                Layout(name="question", size=4),
                Layout(name="spacer", size=2),
                Layout(name="input", size=5),
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
                        box=MINIMAL,
                        padding=(0, 2)
                    )
                )
            )
            
            # Claude Code CLI-style input box
            from rich.box import ROUNDED
            input_box = Panel(
                "",
                title="",
                border_style=self.theme.ORANGE,
                box=ROUNDED,
                padding=(0, 1),
                width=80,
                height=3
            )
            
            layout["input"].update(
                Align.center(input_box)
            )
            
            # Default value hint
            if default:
                default_hint = Text(f"Default: {default}", style=self.theme.TEXT_DIM)
                layout["content"].update(
                    Align.center(default_hint, vertical="top")
                )
            
            # Footer
            layout["footer"].update(
                self._create_footer(hint or "Type your answer and press ENTER")
            )
            
            # Print layout
            self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
            
            # Position cursor inside the input box
            # Move cursor to the input box position
            term_width = self.width
            box_width = 80
            box_left = (term_width - box_width) // 2
            input_row = 19  # Approximate row for input box
            
            # Move cursor to input box position
            print(f'\033[{input_row};{box_left + 3}H', end='', flush=True)
            print('\033[?25h', end='', flush=True)  # Show cursor
            
            # Get input with Claude Code CLI style prompt
            answer = input("> ") or default
            
            # Hide cursor again
            print('\033[?25l', end='', flush=True)
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
            note_text.append("Ctrl+E", style=f"bold {self.theme.ORANGE}")
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
            
            table.add_column("Property", style=self.theme.TEXT_DIM, width=12)
            table.add_column("Value", style=self.theme.WHITE)
            
            for key, value in page_items:
                # Truncate very long values for better display
                value_str = str(value)
                if len(value_str) > 200:
                    value_str = value_str[:197] + "..."
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