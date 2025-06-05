"""Claude Task Queue for efficient concurrent API calls."""

import queue
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from ..utils.logger import get_logger
from ..utils.progress import progress_indicator


class TaskStatus(Enum):
    """Status of a Claude task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class ClaudeTask:
    """Represents a single Claude API task."""

    id: str
    name: str
    prompt: str
    expect_json: bool = True
    timeout: Optional[int] = None
    callback: Optional[Callable] = None
    retry_count: int = 0
    max_retries: int = 3
    result: Optional[Any] = None
    error: Optional[Exception] = None
    status: TaskStatus = TaskStatus.PENDING


class ClaudeTaskQueue:
    """Manages concurrent Claude API calls with progress tracking."""

    def __init__(self, max_workers: int = 3, debug_mode: bool = False):
        """Initialize the task queue.

        Args:
            max_workers: Maximum number of concurrent Claude calls
            debug_mode: Enable debug logging
        """
        self.max_workers = max_workers
        self.logger = get_logger(debug_mode)
        self.tasks: Dict[str, ClaudeTask] = {}
        self.task_queue: queue.Queue[ClaudeTask] = queue.Queue()
        self.results: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._progress_callback: Optional[Callable] = None

    def add_task(
        self,
        task_id: str,
        name: str,
        prompt: str,
        expect_json: bool = True,
        timeout: Optional[int] = None,
        callback: Optional[Callable] = None,
    ) -> None:
        """Add a task to the queue."""
        task = ClaudeTask(
            id=task_id,
            name=name,
            prompt=prompt,
            expect_json=expect_json,
            timeout=timeout,
            callback=callback,
        )

        with self._lock:
            self.tasks[task_id] = task
            self.task_queue.put(task)

        self.logger.debug(f"Added task to queue: {task_id} - {name}")

    def add_batch_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Add multiple tasks at once.

        Args:
            tasks: List of task dictionaries with keys: id, name, prompt, etc.
        """
        for task_data in tasks:
            self.add_task(**task_data)

    def process_tasks(
        self, claude_processor, progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Process all tasks in the queue concurrently.

        Args:
            claude_processor: Instance of ClaudeProcessor
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary mapping task IDs to results
        """
        self._progress_callback = progress_callback
        total_tasks = len(self.tasks)

        if total_tasks == 0:
            return {}

        self.logger.info(f"Processing {total_tasks} Claude tasks with {self.max_workers} workers")

        # Use batch progress indicator
        with progress_indicator.batch_claude_operations(
            total_tasks, f"Processing {total_tasks} Claude Tasks"
        ) as batch_progress:

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                futures: Dict[Future, ClaudeTask] = {}

                while not self.task_queue.empty():
                    try:
                        task = self.task_queue.get_nowait()
                        future = executor.submit(self._process_single_task, task, claude_processor)
                        futures[future] = task
                        self._update_task_status(task.id, TaskStatus.RUNNING)
                    except queue.Empty:
                        break

                # Process completed tasks
                for future in as_completed(futures):
                    task = futures[future]
                    batch_progress.start_operation(f"Processing: {task.name}")

                    try:
                        result = future.result()
                        task.result = result
                        task.status = TaskStatus.COMPLETED
                        self.results[task.id] = result

                        # Call task-specific callback if provided
                        if task.callback:
                            task.callback(result)

                        batch_progress.complete_operation(success=True)
                        self.logger.debug(f"Task completed: {task.id}")

                    except Exception as e:
                        task.error = e
                        task.status = TaskStatus.FAILED
                        self.results[task.id] = None

                        batch_progress.complete_operation(success=False)
                        self.logger.error(f"Task failed: {task.id}", e)

                        # Retry logic
                        if task.retry_count < task.max_retries:
                            task.retry_count += 1
                            task.status = TaskStatus.RETRYING
                            self.task_queue.put(task)
                            self.logger.info(
                                f"Retrying task: {task.id} (attempt {task.retry_count})"
                            )

        return self.results

    def _process_single_task(self, task: ClaudeTask, claude_processor) -> Any:
        """Process a single task."""
        self.logger.debug(f"Processing task: {task.id} - {task.name}")

        try:
            # Add a small delay between calls to avoid rate limiting
            time.sleep(0.5)

            # Call Claude
            response = claude_processor._call_claude(
                prompt=task.prompt,
                timeout=task.timeout,
                expect_json=task.expect_json,
                progress_callback=None,  # Individual progress handled at batch level
            )

            return response

        except Exception as e:
            self.logger.error(f"Error processing task {task.id}: {str(e)}")
            raise

    def _update_task_status(self, task_id: str, status: TaskStatus) -> None:
        """Update the status of a task."""
        with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = status

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the current status of a task."""
        with self._lock:
            task = self.tasks.get(task_id)
            return task.status if task else None

    def get_all_results(self) -> Dict[str, Any]:
        """Get all results."""
        return self.results.copy()

    def get_successful_results(self) -> Dict[str, Any]:
        """Get only successful results."""
        with self._lock:
            return {
                task_id: result
                for task_id, result in self.results.items()
                if self.tasks[task_id].status == TaskStatus.COMPLETED
            }

    def get_failed_tasks(self) -> List[ClaudeTask]:
        """Get list of failed tasks."""
        with self._lock:
            return [task for task in self.tasks.values() if task.status == TaskStatus.FAILED]
