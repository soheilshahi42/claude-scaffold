"""Progress indicator utilities for CLI operations."""

from contextlib import contextmanager
from typing import Optional, Generator
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
import threading


class ProgressIndicator:
    """Manages progress indicators for long-running operations."""
    
    def __init__(self):
        self.console = Console()
        
    @contextmanager
    def claude_thinking(self, description: str = "Claude is thinking") -> Generator[None, None, None]:
        """Show a progress indicator while Claude is processing."""
        messages = [
            f"🤖 {description}...",
            "⚡ Processing your request...",
            "🧠 Analyzing the information...",
            "💡 Generating response...",
            "📝 Formulating answer...",
            "🔄 Almost there...",
        ]
        
        # Create a progress bar with spinner
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True
        ) as progress:
            # Start the main task
            task = progress.add_task(messages[0], total=None)
            
            # Background thread to update messages
            stop_event = threading.Event()
            
            def update_messages():
                msg_index = 0
                while not stop_event.is_set():
                    time.sleep(3)  # Change message every 3 seconds
                    msg_index = (msg_index + 1) % len(messages)
                    progress.update(task, description=messages[msg_index])
            
            update_thread = threading.Thread(target=update_messages, daemon=True)
            update_thread.start()
            
            try:
                yield
            finally:
                stop_event.set()
                update_thread.join(timeout=0.1)
    
    @contextmanager
    def operation(self, description: str, total: Optional[int] = None) -> Generator['ProgressTask', None, None]:
        """Show a progress bar for operations with known steps."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True
        ) as progress:
            task_id = progress.add_task(description, total=total)
            
            class ProgressTask:
                def __init__(self, progress_obj, task_id):
                    self.progress = progress_obj
                    self.task_id = task_id
                    
                def update(self, advance: int = 1, description: Optional[str] = None):
                    """Update the progress."""
                    if description:
                        self.progress.update(self.task_id, description=description)
                    self.progress.update(self.task_id, advance=advance)
                    
                def set_total(self, total: int):
                    """Set the total for the progress bar."""
                    self.progress.update(self.task_id, total=total)
            
            yield ProgressTask(progress, task_id)
    
    def show_retry(self, attempt: int, max_attempts: int, wait_time: int):
        """Show retry information."""
        self.console.print(
            Panel(
                f"⏱️ Timeout occurred. Retrying...\n"
                f"Attempt {attempt}/{max_attempts}\n"
                f"Waiting {wait_time} seconds before retry...",
                title="🔄 Retry in Progress",
                border_style="yellow"
            )
        )
        
        # Show countdown
        with self.console.status(f"Waiting {wait_time} seconds...") as status:
            for i in range(wait_time, 0, -1):
                status.update(f"Retrying in {i} seconds...")
                time.sleep(1)
    
    def show_error(self, message: str, suggestion: Optional[str] = None):
        """Show an error message with optional suggestion."""
        error_text = Text(message, style="bold red")
        if suggestion:
            error_text.append("\n\n💡 Suggestion: ", style="yellow")
            error_text.append(suggestion, style="white")
        
        self.console.print(
            Panel(
                error_text,
                title="❌ Error",
                border_style="red"
            )
        )
    
    def show_success(self, message: str):
        """Show a success message."""
        self.console.print(
            Panel(
                Text(message, style="bold green"),
                title="✅ Success",
                border_style="green"
            )
        )


# Global progress indicator instance
progress_indicator = ProgressIndicator()