"""Tests for task management functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.core.task_manager import TaskManager


class TestTaskManager:
    """Test cases for task management."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.task_manager = TaskManager()
    
    @patch('src.task_manager.TaskManager.interactive_setup')
    def test_add_task_no_config(self, mock_setup):
        """Test adding task when no config exists."""
        mock_setup.load_config.return_value = None
        
        result = self.task_manager.add_task(Path('/test'), 'module', 'task', 'high')
        
        assert result is False
    
    @patch('src.task_manager.TaskManager.interactive_setup')
    def test_add_task_module_not_found(self, mock_setup):
        """Test adding task to non-existent module."""
        mock_setup.load_config.return_value = {
            'modules': [{'name': 'core'}],
            'tasks': []
        }
        
        result = self.task_manager.add_task(Path('/test'), 'nonexistent', 'task', 'high')
        
        assert result is False
    
    @patch('src.task_manager.Path.exists')
    @patch('src.task_manager.Path.write_text')
    @patch('src.task_manager.Path.read_text')
    @patch('src.task_manager.TaskManager.interactive_setup')
    def test_add_task_success(self, mock_setup, mock_read, mock_write, mock_exists):
        """Test successfully adding a task."""
        # Mock configuration
        mock_setup.load_config.return_value = {
            'modules': [{'name': 'core', 'description': 'Core module'}],
            'tasks': []
        }
        
        # Mock file operations
        mock_exists.return_value = True
        mock_read.return_value = """# Core Module

## Tasks

## Testing Strategy
Test content"""
        
        # Mock save_config
        mock_setup.save_config = Mock()
        
        # Add the task
        result = self.task_manager.add_task(Path('/test'), 'core', 'New Task', 'high')
        
        assert result is True
        mock_setup.save_config.assert_called_once()
        
        # Verify task was added to config
        saved_config = mock_setup.save_config.call_args[0][0]
        assert len(saved_config['tasks']) == 1
        assert saved_config['tasks'][0]['title'] == 'New Task'
        assert saved_config['tasks'][0]['module'] == 'core'
        assert saved_config['tasks'][0]['priority'] == 'high'