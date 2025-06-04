"""Enhanced terminal UI components using Rich."""

from typing import List, Optional, Dict, Any, Callable
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table
from rich.style import Style
from rich.box import ROUNDED
import questionary
from questionary import Style as QStyle
from .icons import icons


class MessageType:
    """Message types with their corresponding styles and icons."""
    CLAUDE_QUESTION = {"icon": icons.QUESTION, "border_style": "yellow", "title": "Claude Question"}
    CLAUDE_SUGGESTION = {"icon": icons.INFO, "border_style": "green", "title": "Claude Suggestion"}
    CLAUDE_RESPONSE = {"icon": icons.ROBOT, "border_style": "blue", "title": "Claude Response"}
    USER_MESSAGE = {"icon": icons.CHEVRON, "border_style": "cyan", "title": "User"}
    ERROR_MESSAGE = {"icon": icons.ERROR, "border_style": "red", "title": "Error"}
    INFO_MESSAGE = {"icon": icons.INFO, "border_style": "white", "title": "Information"}
    SUCCESS_MESSAGE = {"icon": icons.SUCCESS, "border_style": "green", "title": "Success"}


class EnhancedTerminalUI:
    """Enhanced terminal UI with fixed input box and styled messages."""
    
    def __init__(self):
        self.console = Console()
        self.messages: List[Dict[str, Any]] = []
        self.layout = Layout()
        self._setup_layout()
        
        # Enhanced questionary style
        self.qstyle = QStyle([
            ('qmark', 'fg:#FF9D00 bold'),
            ('question', 'bold'),
            ('answer', 'fg:#44B4D5 bold'),
            ('pointer', 'fg:#FF9D00 bold'),
            ('highlighted', 'fg:#FF9D00 bold'),
            ('selected', 'fg:#44B4D5'),
            ('separator', 'fg:#808080'),
            ('instruction', 'fg:#808080'),
            ('text', ''),
            ('disabled', 'fg:#808080 italic')
        ])
    
    def _setup_layout(self):
        """Setup the main layout structure."""
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="conversation", ratio=1),
            Layout(name="input", size=5)
        )
        
        # Set header
        header_text = Text(f"{icons.BUILD} Claude Scaffold - Enhanced Interactive Setup", style="bold white", justify="center")
        self.layout["header"].update(Panel(header_text, style="blue"))
        
        # Initialize conversation area
        self.layout["conversation"].update(Panel("", title="Conversation History", border_style="dim"))
        
        # Initialize input area
        self._update_input_area("Ready for input...")
    
    def _update_input_area(self, prompt_text: str = ""):
        """Update the input area with prompt text."""
        input_content = Text()
        input_content.append(f"{icons.CHEVRON} ", style="bold")
        input_content.append(prompt_text, style="white")
        self.layout["input"].update(
            Panel(
                input_content,
                title="Your Input",
                border_style="cyan",
                box=ROUNDED
            )
        )
    
    def add_message(self, content: str, message_type: Dict[str, str]):
        """Add a message to the conversation history."""
        self.messages.append({
            "content": content,
            "type": message_type
        })
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
                title=msg_type["title"],
                border_style=msg_type["border_style"],
                box=ROUNDED,
                padding=(0, 1)
            )
            
            table.add_row(panel)
            table.add_row("")  # Empty row for spacing
        
        # Update the conversation layout
        self.layout["conversation"].update(
            Panel(
                table,
                title="Conversation History",
                border_style="dim",
                box=ROUNDED
            )
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
            answer = questionary.select(
                question,
                choices=choices,
                style=self.qstyle
            ).ask()
        else:
            answer = questionary.text(
                question,
                style=self.qstyle
            ).ask()
        
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
        
        answer = questionary.confirm(
            question,
            default=default,
            style=self.qstyle
        ).ask()
        
        self.add_message("Yes" if answer else "No", MessageType.USER_MESSAGE)
        return answer
    
    def show_module_suggestions(self, modules: List[Dict[str, Any]]):
        """Display module suggestions in a nice format."""
        # Create a table for modules
        table = Table(
            title=f"{icons.MODULE} Suggested Modules",
            show_header=True,
            header_style="bold magenta",
            border_style="blue"
        )
        
        table.add_column("Module", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Key Features", style="yellow")
        
        for module in modules:
            features = "\n".join([f"{icons.BULLET} {f}" for f in module.get("key_features", [])])
            table.add_row(
                module["name"],
                module["description"],
                features
            )
        
        # Create a panel with the table
        panel = Panel(
            table,
            border_style="blue",
            box=ROUNDED,
            padding=(1, 2)
        )
        
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
                header_style="bold cyan",
                border_style="green"
            )
            
            table.add_column("Task", style="white", no_wrap=True)
            table.add_column("Priority", style="yellow", justify="center")
            table.add_column("Status", style="green", justify="center")
            
            for task in module_tasks:
                priority_color = {
                    "high": "red",
                    "medium": "yellow", 
                    "low": "green"
                }.get(task.get("priority", "medium"), "white")
                
                table.add_row(
                    task["title"],
                    f"[{priority_color}]{task.get('priority', 'medium').upper()}[/{priority_color}]",
                    task.get("status", "pending")
                )
            
            panel = Panel(
                table,
                border_style="green",
                box=ROUNDED,
                padding=(1, 2)
            )
            
            self.console.print(panel)