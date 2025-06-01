"""Tests for formatting utilities."""

import pytest
from src.utils.formatters import Formatters


class TestFormatters:
    """Test cases for formatting utilities."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.formatters = Formatters()
    
    def test_organize_tasks_by_module(self):
        """Test organizing tasks by module."""
        tasks = [
            {'title': 'Task 1', 'module': 'core', 'priority': 'high'},
            {'title': 'Task 2', 'module': 'api', 'priority': 'medium'},
            {'title': 'Task 3', 'module': 'core', 'priority': 'low'}
        ]
        
        result = self.formatters.organize_tasks_by_module(tasks)
        
        assert len(result) == 2
        assert 'core' in result
        assert 'api' in result
        assert len(result['core']) == 2
        assert len(result['api']) == 1
    
    def test_format_module_tasks_empty(self):
        """Test formatting empty task list."""
        result = self.formatters.format_module_tasks('test', [])
        assert result == "No tasks assigned to this module yet."
    
    def test_format_module_tasks_with_details(self):
        """Test formatting tasks with Claude-enhanced details."""
        tasks = [{
            'title': 'Test Task',
            'priority': 'high',
            'details': {
                'goal': 'Test goal',
                'requirements': ['Req 1', 'Req 2'],
                'approach': 'Test approach'
            }
        }]
        
        result = self.formatters.format_module_tasks('test', tasks)
        
        assert '### Task 1 – Test Task' in result
        assert '**Priority**: high' in result
        assert '**Goal**: Test goal' in result
        assert '**Requirements**:' in result
        assert '- Req 1' in result
        assert '**Approach**: Test approach' in result
    
    def test_slugify(self):
        """Test text slugification."""
        assert self.formatters.slugify('Hello World') == 'hello_world'
        assert self.formatters.slugify('Test-Case') == 'test_case'
        assert self.formatters.slugify('API/Endpoint') == 'api_endpoint'
    
    def test_format_project_rules(self):
        """Test formatting project rules."""
        project_data = {
            'rules': {
                'suggested': ['Rule 1', 'Rule 2'],
                'custom': ['Custom Rule']
            }
        }
        
        result = self.formatters.format_project_rules(project_data)
        
        assert '- Rule 1' in result
        assert '- Rule 2' in result
        assert '- Custom Rule' in result
    
    def test_format_constraints(self):
        """Test formatting constraints."""
        project_data = {'constraints': ['Python 3.8+', 'PostgreSQL 12+']}
        
        result = self.formatters.format_constraints(project_data)
        
        assert '- Python 3.8+' in result
        assert '- PostgreSQL 12+' in result
    
    def test_format_dependencies_dict(self):
        """Test formatting dependencies as dictionaries."""
        deps = [
            {'name': 'FastAPI', 'purpose': 'Web framework'},
            {'name': 'SQLAlchemy', 'purpose': 'ORM'}
        ]
        
        result = self.formatters.format_dependencies(deps)
        
        assert '- FastAPI: Web framework' in result
        assert '- SQLAlchemy: ORM' in result
    
    def test_format_examples(self):
        """Test formatting examples."""
        examples = [
            {
                'description': 'Basic usage',
                'code': 'print("Hello")'
            }
        ]
        
        result = self.formatters.format_examples(examples)
        
        assert '# Basic usage' in result
        assert 'print("Hello")' in result