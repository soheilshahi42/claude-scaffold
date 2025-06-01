"""Comprehensive tests for the main scaffold module."""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from src.scaffold import ClaudeScaffold


class TestClaudeScaffold:
    """Test cases for the main ClaudeScaffold class."""
    
    @pytest.fixture
    def scaffold(self):
        """Create a ClaudeScaffold instance with mocked dependencies."""
        with patch('src.scaffold.ProjectCreator') as mock_creator, \
             patch('src.scaffold.TaskManager') as mock_manager:
            scaffold = ClaudeScaffold()
            scaffold.project_creator = mock_creator.return_value
            scaffold.task_manager = mock_manager.return_value
            yield scaffold
    
    def test_initialization(self):
        """Test ClaudeScaffold initialization."""
        with patch('src.scaffold.ProjectCreator') as mock_creator, \
             patch('src.scaffold.TaskManager') as mock_manager:
            scaffold = ClaudeScaffold()
            
            # Verify components are created
            mock_creator.assert_called_once()
            mock_manager.assert_called_once()
            assert hasattr(scaffold, 'project_creator')
            assert hasattr(scaffold, 'task_manager')
    
    def test_create_project_success(self, scaffold):
        """Test successful project creation."""
        # Setup
        project_name = "test_project"
        project_path = Path("/tmp/test_project")
        scaffold.project_creator.create_project.return_value = True
        
        # Execute
        result = scaffold.create_project(
            project_name=project_name,
            project_path=project_path,
            force=False,
            interactive=True
        )
        
        # Verify
        assert result is True
        scaffold.project_creator.create_project.assert_called_once_with(
            project_name, project_path, False, True
        )
    
    def test_create_project_failure(self, scaffold):
        """Test project creation failure."""
        # Setup
        scaffold.project_creator.create_project.return_value = False
        
        # Execute
        result = scaffold.create_project("test_project")
        
        # Verify
        assert result is False
    
    def test_create_project_with_defaults(self, scaffold):
        """Test project creation with default parameters."""
        # Setup
        scaffold.project_creator.create_project.return_value = True
        
        # Execute
        result = scaffold.create_project("test_project")
        
        # Verify
        scaffold.project_creator.create_project.assert_called_once_with(
            "test_project", None, False, True
        )
    
    def test_create_project_non_interactive(self, scaffold):
        """Test non-interactive project creation."""
        # Setup
        scaffold.project_creator.create_project.return_value = True
        
        # Execute
        result = scaffold.create_project(
            "test_project",
            interactive=False
        )
        
        # Verify
        scaffold.project_creator.create_project.assert_called_once_with(
            "test_project", None, False, False
        )
    
    def test_add_task_success(self, scaffold):
        """Test successful task addition."""
        # Setup
        project_path = Path("/tmp/test_project")
        module_name = "backend"
        task_title = "Implement authentication"
        priority = "high"
        scaffold.task_manager.add_task.return_value = True
        
        # Execute
        result = scaffold.add_task(
            project_path=project_path,
            module_name=module_name,
            task_title=task_title,
            priority=priority
        )
        
        # Verify
        assert result is True
        scaffold.task_manager.add_task.assert_called_once_with(
            project_path, module_name, task_title, priority
        )
    
    def test_add_task_default_priority(self, scaffold):
        """Test task addition with default priority."""
        # Setup
        project_path = Path("/tmp/test_project")
        scaffold.task_manager.add_task.return_value = True
        
        # Execute
        result = scaffold.add_task(
            project_path=project_path,
            module_name="api",
            task_title="Create endpoints"
        )
        
        # Verify
        scaffold.task_manager.add_task.assert_called_once_with(
            project_path, "api", "Create endpoints", "medium"
        )
    
    def test_add_task_failure(self, scaffold):
        """Test task addition failure."""
        # Setup
        scaffold.task_manager.add_task.return_value = False
        
        # Execute
        result = scaffold.add_task(
            Path("/tmp/test"),
            "module",
            "task"
        )
        
        # Verify
        assert result is False
    
    def test_create_project_exception_handling(self, scaffold):
        """Test exception handling in create_project."""
        # Setup
        scaffold.project_creator.create_project.side_effect = Exception("Test error")
        
        # Execute & Verify
        with pytest.raises(Exception) as exc_info:
            scaffold.create_project("test_project")
        assert str(exc_info.value) == "Test error"
    
    def test_add_task_exception_handling(self, scaffold):
        """Test exception handling in add_task."""
        # Setup
        scaffold.task_manager.add_task.side_effect = Exception("Task error")
        
        # Execute & Verify
        with pytest.raises(Exception) as exc_info:
            scaffold.add_task(Path("/tmp"), "module", "task")
        assert str(exc_info.value) == "Task error"