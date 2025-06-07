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
    
    # Retro CRT effect colors
    SCANLINE = "#111111"
    GLOW = ORANGE_DARK


class RetroUI:
    """Full-screen retro UI for Claude Scaffold."""
    
    def __init__(self):
        self.console = Console()
        self.theme = RetroTheme()
        self.width, self.height = self._get_terminal_size()
        
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
        
    def _get_terminal_size(self) -> Tuple[int, int]:
        """Get terminal dimensions."""
        size = shutil.get_terminal_size()
        return size.columns, size.lines
        
    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
        
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
            Layout(name="header", size=10),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=4)
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
        
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
        input()  # Wait for Enter
        
    def ask_selection(
        self, 
        title: str, 
        question: str, 
        choices: List[Any],
        subtitle: str = "",
        hint: str = ""
    ) -> Any:
        """Show a full-screen selection page."""
        self._clear_screen()
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=10),
            Layout(name="question", size=4),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=4)
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
        
        # Placeholder for choices (will be handled by questionary)
        layout["content"].update(
            Align.center(
                Text("\n\n" + "━" * 60, style=self.theme.GRAY),
                vertical="middle"
            )
        )
        
        # Footer
        layout["footer"].update(self._create_footer(hint))
        
        # Print layout
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
        
        # Move cursor up to the content area for questionary
        self.console.print("\033[15A")  # Move up 15 lines
        
        # Ask question with styled choices
        if isinstance(choices[0], dict):
            # Choices with names and values
            q_choices = [
                questionary.Choice(
                    title=choice.get("name", str(choice)),
                    value=choice.get("value", choice)
                )
                for choice in choices
            ]
        else:
            q_choices = choices
            
        answer = questionary.select(
            "",  # Empty question since we already displayed it
            choices=q_choices,
            style=self.qstyle
        ).ask()
        
        return answer
        
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
            Layout(name="header", size=10),
            Layout(name="question", size=4),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=4)
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
        
        # Print layout
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
        
        # Move cursor to input area
        self.console.print("\033[12A")  # Move up
        
        # Get input
        answer = questionary.text(
            "",
            default=default,
            multiline=multiline,
            style=self.qstyle
        ).ask()
        
        return answer
        
    def ask_confirm(
        self,
        title: str,
        question: str,
        default: bool = False,
        subtitle: str = "",
        hint: str = ""
    ) -> bool:
        """Show a full-screen confirmation page."""
        self._clear_screen()
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=10),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=4)
        )
        
        # Header
        layout["header"].update(
            self._create_header(title, subtitle)
        )
        
        # Content
        confirm_text = Text()
        confirm_text.append("\n\n? ", style=f"bold {self.theme.ORANGE}")
        confirm_text.append(question, style=f"bold {self.theme.WHITE}")
        confirm_text.append("\n\n")
        
        # Yes/No options
        options = Text()
        options.append("  ▶ ", style=self.theme.ORANGE if default else self.theme.GRAY)
        options.append("Yes", style=f"bold {self.theme.WHITE if default else self.theme.TEXT_DIM}")
        options.append("     ")
        options.append("  ▶ ", style=self.theme.GRAY if default else self.theme.ORANGE)
        options.append("No", style=f"bold {self.theme.TEXT_DIM if default else self.theme.WHITE}")
        
        content = Panel(
            Align.center(Group(confirm_text, options), vertical="middle"),
            border_style=self.theme.ORANGE_DARK,
            box=DOUBLE,
            padding=(2, 4)
        )
        
        layout["content"].update(
            Align.center(content, vertical="middle")
        )
        
        # Footer
        layout["footer"].update(
            self._create_footer(hint or "Use arrow keys to select, Enter to confirm")
        )
        
        # Print layout
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
        
        # Get confirmation
        answer = questionary.confirm(
            "",
            default=default,
            style=self.qstyle
        ).ask()
        
        return answer
        
    def show_progress(
        self,
        title: str,
        message: str,
        subtitle: str = "",
        items: Optional[List[str]] = None
    ):
        """Show a full-screen progress page."""
        self._clear_screen()
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=10),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=4)
        )
        
        # Header
        layout["header"].update(
            self._create_header(title, subtitle)
        )
        
        # Progress content
        progress_text = Text()
        progress_text.append(f"\n{message}\n\n", style=f"bold {self.theme.WHITE}")
        
        if items:
            for item in items:
                progress_text.append(f"  {icons.PROGRESS} ", style=self.theme.ORANGE)
                progress_text.append(f"{item}\n", style=self.theme.TEXT_DIM)
                
        # Animated loading indicator
        progress_text.append("\n\n")
        progress_text.append("█" * 20, style=self.theme.ORANGE_DARK)
        progress_text.append("█" * 10, style=self.theme.ORANGE)
        progress_text.append("░" * 10, style=self.theme.GRAY)
        
        content = Panel(
            Align.center(progress_text, vertical="middle"),
            title=f"[{self.theme.ORANGE}]▶ PROCESSING[/]",
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
            Layout(name="header", size=10),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=4)
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
        
        # Print layout
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
        
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
            input()  # Wait for Enter
            
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
            Layout(name="header", size=10),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=4)
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
        
        # Print layout
        self.console.print(layout, style=f"on {self.theme.BACKGROUND}")
        input()  # Wait for Enter