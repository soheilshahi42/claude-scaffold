"""Main scaffold module that delegates to specialized components."""

from .core.project_creator import ProjectCreator
from .core.task_manager import TaskManager


class ClaudeScaffold:
    """Enhanced Claude Scaffold with comprehensive project generation."""
    
    def __init__(self, debug_mode: bool = False):
        self.project_creator = ProjectCreator(debug_mode=debug_mode)
        self.task_manager = TaskManager()
    
    def create_project(self, project_name, project_path=None, force=False, interactive=True):
        """Create a new Claude Scaffold project."""
        return self.project_creator.create_project(project_name, project_path, force, interactive)
    
    def add_task(self, project_path, module_name, task_title, priority='medium'):
        """Add a new task to an existing project."""
        return self.task_manager.add_task(project_path, module_name, task_title, priority)