"""Enhanced terminal UI components using Rich."""

from typing import Any, Dict, List, Optional

import questionary
from questionary import Style as QStyle
from rich.box import MINIMAL
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .icons import icons


class MessageType:
    """Message types with their corresponding styles and icons."""

    CLAUDE_QUESTION = {
        "icon": "🤖",
        "border_style": "bright_black",
        "title": "Claude",
    }
    CLAUDE_SUGGESTION = {
        "icon": "💡",
        "border_style": "bright_black",
        "title": "Suggestion",
    }
    CLAUDE_RESPONSE = {
        "icon": "🤖",
        "border_style": "bright_black",
        "title": "Claude",
    }
    USER_MESSAGE = {"icon": "👤", "border_style": "bright_black", "title": "You"}
    ERROR_MESSAGE = {"icon": "❌", "border_style": "red", "title": "Error"}
    INFO_MESSAGE = {"icon": "ℹ️", "border_style": "bright_black", "title": "Info"}
    SUCCESS_MESSAGE = {
        "icon": "✅",
        "border_style": "green",
        "title": "Success",
    }


class EnhancedTerminalUI:
    """Enhanced terminal UI with fixed input box and styled messages."""

    def __init__(self):
        self.console = Console()
        self.messages: List[Dict[str, Any]] = []
        self.layout = Layout()
        self._setup_layout()

        # Minimal questionary style matching Claude Code
        self.qstyle = QStyle(
            [
                ("qmark", "fg:#666666"),
                ("question", ""),
                ("answer", "fg:#0066cc"),
                ("pointer", "fg:#0066cc"),
                ("highlighted", "fg:#0066cc"),
                ("selected", "fg:#0066cc"),
                ("separator", "fg:#666666"),
                ("instruction", "fg:#666666"),
                ("text", ""),
                ("disabled", "fg:#999999"),
            ]
        )

    def _setup_layout(self):
        """Setup the main layout structure."""
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="conversation", ratio=1),
            Layout(name="input", size=5),
        )

        # Set header
        header_text = Text(
            "claude-scaffold",
            style="dim",
            justify="left",
        )
        self.layout["header"].update(Panel(header_text, style="bright_black", box=None, padding=(0, 1)))

        # Initialize conversation area
        self.layout["conversation"].update(
            Panel("", border_style="bright_black", box=None)
        )

        # Initialize input area
        self._update_input_area("Ready for input...")

    def _update_input_area(self, prompt_text: str = ""):
        """Update the input area with prompt text."""
        input_content = Text()
        input_content.append("› ", style="bright_black")
        input_content.append(prompt_text, style="")
        self.layout["input"].update(
            Panel(input_content, border_style="bright_black", box=MINIMAL, padding=(0, 1))
        )

    def add_message(self, content: str, message_type: Dict[str, str]):
        """Add a message to the conversation history."""
        self.messages.append({"content": content, "type": message_type})
        self._update_conversation_display()

    def _update_conversation_display(self):
        """Update the conversation display with all messages."""
        # Create a table for messages
        table = Table(show_header=False, show_edge=False, pad_edge=False, box=None)
        table.add_column("Messages", style="white")

        # Add all messages
        for msg in self.messages[-20:]:  # Show last 20 messages
            msg_type = msg["type"]

            # Create message panel
            content = Text()
            content.append(f"{msg_type['icon']} ", style="bold")
            content.append(msg["content"])

            panel = Panel(
                content,
                border_style=msg_type["border_style"],
                box=MINIMAL,
                padding=(0, 1),
            )

            table.add_row(panel)
            table.add_row("")  # Empty row for spacing

        # Update the conversation layout
        self.layout["conversation"].update(
            Panel(table, border_style="dim", box=MINIMAL, padding=(0, 1))
        )

    def display(self):
        """Display the layout."""
        self.console.print(self.layout)

    def clear_screen(self):
        """Clear the terminal screen."""
        self.console.clear()

    def ask_question(self, question: str, choices: Optional[List[str]] = None) -> str:
        """Ask a question with optional choices."""
        # Add the question to conversation
        self.add_message(question, MessageType.CLAUDE_QUESTION)

        # Clear and redisplay
        self.clear_screen()
        self.display()

        # Update input area
        self._update_input_area("Type your answer below...")

        # Use questionary for input
        if choices:
            answer = questionary.select(question, choices=choices, style=self.qstyle).ask()
        else:
            answer = questionary.text(question, style=self.qstyle).ask()

        # Add user answer to conversation
        if answer:
            self.add_message(answer, MessageType.USER_MESSAGE)

        return answer

    def show_suggestion(self, suggestion: str):
        """Show a suggestion from Claude."""
        self.add_message(suggestion, MessageType.CLAUDE_SUGGESTION)
        self.clear_screen()
        self.display()

    def show_response(self, response: str):
        """Show a response from Claude."""
        self.add_message(response, MessageType.CLAUDE_RESPONSE)
        self.clear_screen()
        self.display()

    def show_error(self, error: str):
        """Show an error message."""
        self.add_message(error, MessageType.ERROR_MESSAGE)
        self.clear_screen()
        self.display()

    def show_info(self, info: str):
        """Show an info message."""
        self.add_message(info, MessageType.INFO_MESSAGE)
        self.clear_screen()
        self.display()

    def show_success(self, message: str):
        """Show a success message."""
        self.add_message(message, MessageType.SUCCESS_MESSAGE)
        self.clear_screen()
        self.display()

    def confirm(self, question: str, default: bool = False) -> bool:
        """Ask for confirmation."""
        self.add_message(question, MessageType.CLAUDE_QUESTION)
        self.clear_screen()
        self.display()

        answer = questionary.confirm(question, default=default, style=self.qstyle).ask()

        self.add_message("Yes" if answer else "No", MessageType.USER_MESSAGE)
        return answer

    def show_module_suggestions(self, modules: List[Dict[str, Any]]):
        """Display module suggestions in a nice format."""
        # Create a table for modules
        table = Table(
            title=f"{icons.MODULE} Modules",
            show_header=True,
            header_style="",
            border_style="bright_black",
            box=MINIMAL,
        )

        table.add_column("Module", style="", no_wrap=True)
        table.add_column("Description", style="dim")
        table.add_column("Key Features", style="dim")

        for module in modules:
            features = "\n".join([f"{icons.BULLET} {f}" for f in module.get("key_features", [])])
            table.add_row(module["name"], module["description"], features)

        # Create a panel with the table
        panel = Panel(table, border_style="bright_black", box=MINIMAL, padding=(1, 2))

        self.console.print(panel)

    def show_task_list(self, tasks: List[Dict[str, Any]]):
        """Display task list in a nice format."""
        # Group tasks by module
        tasks_by_module = {}
        for task in tasks:
            module = task.get("module", "General")
            if module not in tasks_by_module:
                tasks_by_module[module] = []
            tasks_by_module[module].append(task)

        # Create panels for each module
        for module, module_tasks in tasks_by_module.items():
            table = Table(
                title=f"{icons.TASK} {module} Tasks",
                show_header=True,
                header_style="",
                border_style="bright_black",
                box=MINIMAL,
            )

            table.add_column("Task", style="", no_wrap=True)
            table.add_column("Priority", style="dim", justify="center")
            table.add_column("Status", style="dim", justify="center")

            for task in module_tasks:
                status = task.get("status", "pending")
                status_style = (
                    "green"
                    if status.lower() == "completed"
                    else "yellow"
                    if status.lower() == "in_progress"
                    else "red"
                )
                table.add_row(
                    task["title"],
                    f"[{status_style}]{status}[/{status_style}]",
                )

            panel = Panel(table, border_style="bright_black", box=MINIMAL, padding=(1, 2))

            self.console.print(panel)
