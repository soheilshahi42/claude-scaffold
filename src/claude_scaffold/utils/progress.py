"""Progress indicator utilities for CLI operations."""

import threading
import time
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generator, Optional

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from .icons import icons


class ProgressIndicator:
    """Manages progress indicators for long-running operations."""

    def __init__(self):
        self.console = Console()

    @contextmanager
    def claude_thinking(
        self, description: str = "Claude is thinking", show_details: bool = True
    ) -> Generator["Any", None, None]:
        """Show an enhanced progress indicator while Claude is processing."""
        messages = [
            f"{icons.ROBOT} {description}...",
            f"{icons.LIGHTNING} Processing your request...",
            f"{icons.ANALYZE} Analyzing the information...",
            f"{icons.THINKING} Generating response...",
            f"{icons.DOCUMENT} Formulating answer...",
            f"{icons.PROGRESS} Almost there...",
        ]

        # Create a layout for detailed progress
        layout = Layout()
        layout.split_column(
            Layout(name="main", size=3),
            Layout(name="details", size=4),
        )

        # Progress information
        start_time = datetime.now()
        status_details = {
            "prompt_size": "Unknown",
            "status": "Initializing",
            "elapsed": "0s",
            "phase": "Starting",
        }

        # Create progress bar
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=30),
            TimeElapsedColumn(),
            console=self.console,
            transient=False,
        )

        task = progress.add_task(messages[0], total=100)

        # Background thread to update UI
        stop_event = threading.Event()

        def update_display():
            msg_index = 0
            progress_value = 0

            with Live(
                layout if show_details else progress,
                console=self.console,
                refresh_per_second=4,
            ) as live:
                while not stop_event.is_set():
                    # Update elapsed time
                    elapsed = (datetime.now() - start_time).total_seconds()
                    status_details["elapsed"] = f"{elapsed:.1f}s"

                    # Update progress message
                    if elapsed > 3:
                        msg_index = min(int(elapsed / 3), len(messages) - 1)
                        progress.update(task, description=messages[msg_index])

                    # Update progress bar
                    if progress_value < 90:
                        progress_value += 2
                        progress.update(task, completed=progress_value)

                    # Update layout if showing details
                    if show_details:
                        # Main panel
                        main_panel = Panel(
                            progress,
                            title=f"{icons.ROBOT} Claude Processing",
                            border_style="blue",
                        )
                        layout["main"].update(main_panel)

                        # Details table
                        details_table = Table(show_header=False, box="minimal", padding=(0, 1))
                        details_table.add_column("Key", style="cyan", width=15)
                        details_table.add_column("Value", style="white")

                        details_table.add_row(f"{icons.INFO} Status:", status_details["status"])
                        details_table.add_row(
                            f"{icons.DOCUMENT} Prompt Size:",
                            status_details["prompt_size"],
                        )
                        details_table.add_row(f"{icons.CLOCK} Elapsed:", status_details["elapsed"])
                        details_table.add_row(f"{icons.PROGRESS} Phase:", status_details["phase"])

                        details_panel = Panel(details_table, title="Details", border_style="dim")
                        layout["details"].update(details_panel)

                        live.update(layout)
                    else:
                        live.update(progress)

                    time.sleep(0.25)

                # Final update
                progress.update(task, completed=100, description=f"{icons.SUCCESS} Complete!")
                time.sleep(0.5)

        update_thread = threading.Thread(target=update_display, daemon=True)
        update_thread.start()

        class Any:
            def __init__(self, details_dict, stop_evt):
                self.details = details_dict
                self.stop_event = stop_evt

            def update_status(self, status: str, phase: Optional[str] = None):
                """Update the current status."""
                self.details["status"] = status
                if phase:
                    self.details["phase"] = phase

            def set_prompt_size(self, size: int):
                """Set the prompt size."""
                self.details["prompt_size"] = f"{size:,} chars"

        try:
            yield Any(status_details, stop_event)
        finally:
            stop_event.set()
            update_thread.join(timeout=0.5)

    @contextmanager
    def operation(
        self, description: str, total: Optional[int] = None
    ) -> Generator["Any", None, None]:
        """Show a progress bar for operations with known steps."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
        ) as progress:
            task_id = progress.add_task(description, total=total)

            class Any:
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

            yield Any(progress, task_id)

    def show_retry(self, attempt: int, max_attempts: int, wait_time: int):
        """Show retry information."""
        self.console.print(
            Panel(
                f"{icons.CLOCK} Timeout occurred. Retrying...\n"
                f"Attempt {attempt}/{max_attempts}\n"
                f"Waiting {wait_time} seconds before retry...",
                title=f"{icons.PROGRESS} Retry in Progress",
                border_style="yellow",
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
            error_text.append(f"\n\n{icons.INFO} Suggestion: ", style="yellow")
            error_text.append(suggestion, style="white")

        self.console.print(Panel(error_text, title=f"{icons.ERROR} Error", border_style="red"))

    def show_success(self, message: str):
        """Show a success message."""
        self.console.print(
            Panel(
                Text(message, style="bold green"),
                title=f"{icons.SUCCESS} Success",
                border_style="green",
            )
        )

    def show_claude_status(self, status: str, detail: Optional[str] = None):
        """Show a quick Claude status update."""
        status_text = f"{icons.ROBOT} {status}"
        if detail:
            status_text += f" - {detail}"
        self.console.print(status_text, style="blue")

    @contextmanager
    def batch_claude_operations(
        self, total_operations: int, title: str = "Processing with Claude"
    ) -> Generator["Any", None, None]:
        """Show progress for multiple Claude operations."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="progress", size=5),
            Layout(name="current", size=4),
        )

        # Overall progress
        overall_progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeElapsedColumn(),
        )

        # Current operation progress
        current_progress = Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            TimeElapsedColumn(),
        )

        overall_task = overall_progress.add_task("Overall Progress", total=total_operations)
        current_task = current_progress.add_task("Initializing...", total=None)

        # State tracking
        state = {
            "completed": 0,
            "current_operation": "Initializing",
            "start_time": datetime.now(),
            "errors": 0,
        }

        class Any:
            def __init__(
                self,
                overall_prog,
                current_prog,
                overall_id,
                current_id,
                state_dict,
                console,
            ):
                self.overall_progress = overall_prog
                self.current_progress = current_prog
                self.overall_task = overall_id
                self.current_task = current_id
                self.state = state_dict
                self.console = console

            def start_operation(self, description: str):
                """Start a new operation."""
                self.state["current_operation"] = description
                self.current_progress.update(self.current_task, description=description)

            def complete_operation(self, success: bool = True):
                """Mark current operation as complete."""
                self.state["completed"] += 1
                if not success:
                    self.state["errors"] += 1
                self.overall_progress.update(self.overall_task, advance=1)

            def update_current(self, message: str):
                """Update current operation message."""
                self.current_progress.update(self.current_task, description=message)

        # Don't use Live display if we're already in one
        if hasattr(self.console, "_live") and self.console._live:
            # Just yield a simple batch progress without Live display
            batch_progress = Any(None, None, None, None, state, self.console)

            def start_op(desc):
                state["current_operation"] = desc
                self.console.print(f"{icons.PROGRESS} {desc}")

            def complete_op(success=True):
                state["completed"] += 1
                if not success:
                    state["errors"] += 1

            batch_progress.start_operation = start_op
            batch_progress.complete_operation = complete_op
            batch_progress.update_current = lambda msg: None
            try:
                yield batch_progress
            finally:
                self.console.print(
                    f"{icons.SUCCESS} Completed {state['completed']}/{total_operations} operations"
                )
            return

        # Create a separate console for batch operations to avoid conflicts
        batch_console = Console()

        with Live(layout, console=batch_console, refresh_per_second=4):
            # Header
            header_text = Text(f"{icons.ROBOT} {title}", style="bold blue", justify="center")
            header_panel = Panel(header_text, border_style="blue")
            layout["header"].update(header_panel)

            # Progress panel
            progress_panel = Panel(overall_progress, title="Progress", border_style="cyan")
            layout["progress"].update(progress_panel)

            # Current operation panel
            current_panel = Panel(
                current_progress, title="Current Operation", border_style="yellow"
            )
            layout["current"].update(current_panel)

            batch_progress = Any(
                overall_progress,
                current_progress,
                overall_task,
                current_task,
                state,
                batch_console,
            )

            try:
                yield batch_progress
            finally:
                # Show final summary
                elapsed = (datetime.now() - state["start_time"]).total_seconds()
                summary = f"Completed {state['completed']}/{total_operations} operations in {elapsed:.1f}s"
                if state["errors"] > 0:
                    summary += f" ({state['errors']} errors)"

                self.console.print(
                    Panel(
                        Text(
                            summary,
                            style="bold green" if state["errors"] == 0 else "yellow",
                        ),
                        title=(
                            f"{icons.SUCCESS} Batch Complete"
                            if state["errors"] == 0
                            else f"{icons.WARNING} Batch Complete with Errors"
                        ),
                        border_style="green" if state["errors"] == 0 else "yellow",
                    )
                )


# Global progress indicator instance
progress_indicator = ProgressIndicator()
