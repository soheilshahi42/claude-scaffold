"""Unified UI/UX manager for consistent progress tracking and user feedback."""

import time
from typing import Optional, Callable, Any, Dict, List
from contextlib import contextmanager
from datetime import datetime

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich import box

from .icons import Icons
from .terminal_ui import EnhancedTerminalUI


class UIManager:
    """Manages all UI/UX operations with consistent progress tracking."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.terminal_ui = EnhancedTerminalUI()
        self.operation_timings: Dict[str, float] = {}
        self.start_time = datetime.now()

    @contextmanager
    def step_progress(
        self, title: str, total_steps: Optional[int] = None, show_timing: bool = True
    ):
        """Context manager for tracking step-by-step progress with timing."""
        start_time = time.time()

        # Create progress bar with appropriate columns
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.console,
            transient=False,
        )

        # Add main task
        if total_steps:
            task_id = progress.add_task(f"{Icons.PROGRESS} {title}", total=total_steps)
        else:
            task_id = progress.add_task(f"{Icons.PROGRESS} {title}", total=None)

        class StepTracker:
            def __init__(self, progress_obj, task_id, manager):
                self.progress = progress_obj
                self.task_id = task_id
                self.manager = manager
                self.current_step = 0
                self.step_timings = []

            def update(self, description: str, advance: int = 1):
                """Update current step with timing."""
                step_start = time.time()
                self.progress.update(
                    self.task_id, description=f"{Icons.PROGRESS} {description}"
                )
                if total_steps:
                    self.progress.update(self.task_id, advance=advance)
                self.current_step += advance

                # Record timing
                if self.step_timings:
                    last_timing = time.time() - step_start
                    self.step_timings.append((description, last_timing))

            def complete(self, message: Optional[str] = None):
                """Mark as complete with success icon."""
                if message:
                    self.progress.update(
                        self.task_id, description=f"{Icons.SUCCESS} {message}"
                    )
                else:
                    self.progress.update(
                        self.task_id, description=f"{Icons.SUCCESS} {title} completed"
                    )
                if total_steps:
                    self.progress.update(self.task_id, completed=total_steps)

            def set_total(self, new_total: int):
                """Update the total number of steps."""
                self.progress.update(self.task_id, total=new_total)

            def error(self, message: str):
                """Mark as error."""
                self.progress.update(
                    self.task_id, description=f"{Icons.ERROR} {message}"
                )

        tracker = StepTracker(progress, task_id, self)

        with progress:
            try:
                yield tracker
                # Auto-complete if not already done
                if progress.tasks[task_id].completed != progress.tasks[task_id].total:
                    tracker.complete()
            except Exception as e:
                tracker.error(f"Failed: {str(e)}")
                raise
            finally:
                # Record total timing
                elapsed = time.time() - start_time
                self.operation_timings[title] = elapsed

                if show_timing:
                    self.console.print(
                        f"   {Icons.CLOCK} Completed in {elapsed:.2f}s", style="dim"
                    )

    @contextmanager
    def live_status(self, title: str, show_details: bool = True):
        """Live updating status display with details panel."""
        layout = Layout()

        if show_details:
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="status", size=3),
                Layout(name="details", ratio=1),
            )
        else:
            layout.split_column(
                Layout(name="header", size=3), Layout(name="status", size=3)
            )

        # Header
        header_text = Text(
            f"{Icons.BUILD} {title}", style="bold cyan", justify="center"
        )
        layout["header"].update(Panel(header_text, box=box.DOUBLE))

        # Status tracking
        status_info = {
            "current": "Initializing...",
            "elapsed": 0,
            "details": {},
            "progress": 0,
        }

        start_time = time.time()

        class StatusUpdater:
            def __init__(self, layout_obj, status_dict, show_details_flag):
                self.layout = layout_obj
                self.status = status_dict
                self.show_details = show_details_flag

            def update(self, message: str, progress: Optional[int] = None, **details):
                """Update status and optional details."""
                self.status["current"] = message
                if progress is not None:
                    self.status["progress"] = progress

                # Update details
                for key, value in details.items():
                    self.status["details"][key] = value

                self._refresh_display()

            def _refresh_display(self):
                """Refresh the display with current status."""
                # Update elapsed time
                self.status["elapsed"] = time.time() - start_time

                # Status panel
                status_text = Text()
                status_text.append(f"{Icons.PROGRESS} ", style="cyan")
                status_text.append(self.status["current"], style="white")
                status_text.append(f"\n{Icons.CLOCK} ", style="yellow")
                status_text.append(
                    f"Elapsed: {self.status['elapsed']:.1f}s", style="white"
                )

                if self.status["progress"] > 0:
                    status_text.append(f"\n{Icons.CHART} ", style="green")
                    status_text.append(
                        f"Progress: {self.status['progress']}%", style="white"
                    )

                self.layout["status"].update(
                    Panel(status_text, title="Status", border_style="cyan")
                )

                # Details panel (if enabled)
                if self.show_details and self.status["details"]:
                    details_table = Table(show_header=False, box=None)
                    details_table.add_column("Key", style="cyan", width=20)
                    details_table.add_column("Value", style="white")

                    for key, value in self.status["details"].items():
                        details_table.add_row(f"{Icons.BULLET} {key}:", str(value))

                    self.layout["details"].update(
                        Panel(details_table, title="Details", border_style="dim")
                    )

            def success(self, message: str):
                """Mark operation as successful."""
                self.status["current"] = f"{Icons.SUCCESS} {message}"
                self.status["progress"] = 100
                self._refresh_display()

            def error(self, message: str):
                """Mark operation as failed."""
                self.status["current"] = f"{Icons.ERROR} {message}"
                self._refresh_display()

        updater = StatusUpdater(layout, status_info, show_details)

        with Live(layout, console=self.console, refresh_per_second=4):
            try:
                yield updater
                updater.success(f"{title} completed successfully")
                time.sleep(0.5)  # Brief pause to show completion
            except Exception as e:
                updater.error(f"Failed: {str(e)}")
                time.sleep(1)  # Show error briefly
                raise

    def show_summary(
        self, title: str, items: List[Dict[str, Any]], show_timing: bool = True
    ):
        """Show a summary panel with optional timing information."""
        # Create summary table
        table = Table(
            title=f"{Icons.INFO} {title}",
            show_header=True,
            header_style="bold cyan",
            border_style="blue",
            box=box.ROUNDED,
        )

        # Add columns based on first item
        if items and len(items) > 0:
            for key in items[0].keys():
                table.add_column(key.replace("_", " ").title(), style="white")

            # Add rows
            for item in items:
                row_values = []
                for key, value in item.items():
                    # Format special values
                    if key == "status":
                        if value == "completed":
                            row_values.append(f"[green]{Icons.SUCCESS} {value}[/green]")
                        elif value == "pending":
                            row_values.append(f"[yellow]{Icons.CLOCK} {value}[/yellow]")
                        elif value == "error":
                            row_values.append(f"[red]{Icons.ERROR} {value}[/red]")
                        else:
                            row_values.append(str(value))
                    elif key == "priority":
                        icon = Icons.get_priority_icon(str(value))
                        color = {"high": "red", "medium": "yellow", "low": "green"}.get(
                            str(value), "white"
                        )
                        row_values.append(f"[{color}]{icon} {value}[/{color}]")
                    else:
                        row_values.append(str(value))

                table.add_row(*row_values)

        # Add timing summary if available
        if show_timing and self.operation_timings:
            table.add_section()
            table.add_row(*[""] * len(items[0].keys())) if items else None

            timing_text = (
                f"{Icons.CLOCK} Total time: {sum(self.operation_timings.values()):.2f}s"
            )
            if len(items[0].keys()) > 1:
                table.add_row(timing_text, *[""] * (len(items[0].keys()) - 1))
            else:
                table.add_row(timing_text)

        # Display the panel
        self.console.print(Panel(table, border_style="blue", padding=(1, 2)))

    def show_progress_spinner(self, message: str, task: Callable[[], Any]) -> Any:
        """Show a simple spinner while executing a task."""
        with self.console.status(f"{Icons.LOADING} {message}...") as status:
            result = task()
            status.update(f"{Icons.SUCCESS} {message} - Done!")
            time.sleep(0.3)  # Brief pause to show completion
        return result

    def prompt_with_progress(
        self, prompt: str, validator: Optional[Callable[[str], bool]] = None
    ) -> str:
        """Prompt user with progress indication."""
        with self.console.status(f"{Icons.THINKING} Waiting for input..."):
            # Clear status for input
            self.console.print(f"\n{Icons.QUESTION} {prompt}")

            while True:
                user_input = input(f"{Icons.CHEVRON} ")

                if validator:
                    if validator(user_input):
                        return user_input
                    else:
                        self.console.print(
                            f"{Icons.ERROR} Invalid input. Please try again.",
                            style="red",
                        )
                else:
                    return user_input

    def show_operation_summary(self):
        """Show a summary of all operations with timings."""
        if not self.operation_timings:
            return

        # Create timing table
        table = Table(
            title=f"{Icons.CHART} Operation Summary",
            show_header=True,
            header_style="bold magenta",
            border_style="magenta",
        )

        table.add_column("Operation", style="cyan", no_wrap=True)
        table.add_column("Time (s)", style="yellow", justify="right")
        table.add_column("Percentage", style="green", justify="right")

        total_time = sum(self.operation_timings.values())

        # Sort by time descending
        sorted_ops = sorted(
            self.operation_timings.items(), key=lambda x: x[1], reverse=True
        )

        for op_name, op_time in sorted_ops:
            percentage = (op_time / total_time) * 100 if total_time > 0 else 0
            table.add_row(op_name, f"{op_time:.2f}", f"{percentage:.1f}%")

        table.add_section()
        table.add_row(
            "[bold]Total[/bold]",
            f"[bold]{total_time:.2f}[/bold]",
            "[bold]100.0%[/bold]",
        )

        # Add overall metrics
        elapsed_total = (datetime.now() - self.start_time).total_seconds()
        efficiency = (total_time / elapsed_total * 100) if elapsed_total > 0 else 100

        metrics_text = Text()
        metrics_text.append(f"\n{Icons.INFO} Total elapsed time: ", style="cyan")
        metrics_text.append(f"{elapsed_total:.2f}s\n", style="white")
        metrics_text.append(f"{Icons.CHART} Operation efficiency: ", style="cyan")
        metrics_text.append(
            f"{efficiency:.1f}%", style="green" if efficiency > 80 else "yellow"
        )

        self.console.print(Panel(table, border_style="magenta", padding=(1, 2)))
        self.console.print(metrics_text)


# Global UI manager instance
ui_manager = UIManager()
