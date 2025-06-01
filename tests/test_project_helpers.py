"""Tests for project helper functions."""

import pytest
from datetime import datetime
from src.project_helpers import ProjectHelpers


class TestProjectHelpers:
    """Test cases for project helper functions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.helpers = ProjectHelpers()
    
    def test_get_default_project_data(self):
        """Test getting default project data."""
        project_name = "test_project"
        data = self.helpers.get_default_project_data(project_name)
        
        assert data['project_name'] == project_name
        assert 'timestamp' in data
        assert data['version'] == '0.1.0'
        assert len(data['modules']) == 1
        assert data['modules'][0]['name'] == 'core'
        assert data['tasks'] == []
        assert 'metadata' in data
    
    def test_prepare_template_context(self):
        """Test preparing template context."""
        project_data = {
            'project_name': 'test',
            'tasks': [
                {'title': 'Task 1', 'priority': 'high'},
                {'title': 'Task 2', 'priority': 'medium'},
                {'title': 'Task 3', 'priority': 'low'}
            ],
            'modules': [{'name': 'core', 'description': 'Core module'}],
            'metadata': {
                'description': 'Test project',
                'language': 'Python',
                'style_guide': 'pep8'
            }
        }
        
        context = self.helpers.prepare_template_context(project_data)
        
        assert context['project_name'] == 'test'
        assert context['high_priority'] == 1
        assert context['medium_priority'] == 1
        assert context['low_priority'] == 1
        assert context['total_tasks'] == 3
        assert 'timestamp' in context
    
    def test_get_naming_conventions_pep8(self):
        """Test getting naming conventions for PEP8."""
        project_data = {'metadata': {'style_guide': 'pep8'}}
        
        result = self.helpers.get_naming_conventions(project_data)
        
        assert 'PascalCase' in result
        assert 'snake_case' in result
        assert 'UPPER_SNAKE_CASE' in result
    
    def test_get_naming_conventions_custom(self):
        """Test getting naming conventions for custom style."""
        project_data = {'metadata': {'style_guide': 'custom'}}
        
        result = self.helpers.get_naming_conventions(project_data)
        
        assert 'GLOBAL_RULES.md' in result
    
    def test_get_style_conventions_pep8(self):
        """Test getting style conventions for PEP8."""
        project_data = {'metadata': {'style_guide': 'pep8', 'language': 'Python'}}
        
        result = self.helpers.get_style_conventions(project_data)
        
        assert 'Follow PEP 8 strictly' in result
        assert '79 characters' in result
        assert 'type hints' in result
    
    def test_get_style_conventions_black(self):
        """Test getting style conventions for Black."""
        project_data = {'metadata': {'style_guide': 'black', 'language': 'Python'}}
        
        result = self.helpers.get_style_conventions(project_data)
        
        assert 'Black formatter' in result
        assert 'line length: 88' in result
    
    def test_get_architecture_patterns(self):
        """Test getting architecture patterns for different project types."""
        # Web project
        web_data = {'metadata': {'project_type': 'web'}}
        result = self.helpers.get_architecture_patterns(web_data)
        assert 'MVC/MVP' in result
        
        # CLI project
        cli_data = {'metadata': {'project_type': 'cli'}}
        result = self.helpers.get_architecture_patterns(cli_data)
        assert 'Command pattern' in result
        
        # Custom project
        custom_data = {'metadata': {'project_type': 'custom'}}
        result = self.helpers.get_architecture_patterns(custom_data)
        assert 'SOLID principles' in result
    
    def test_get_project_specific_ignores(self):
        """Test getting project-specific gitignore entries."""
        # Web project
        web_data = {'metadata': {'project_type': 'web'}}
        result = self.helpers.get_project_specific_ignores(web_data)
        assert 'node_modules/' in result
        
        # ML project
        ml_data = {'metadata': {'project_type': 'ml'}}
        result = self.helpers.get_project_specific_ignores(ml_data)
        assert 'data/raw/' in result
        
        # API project
        api_data = {'metadata': {'project_type': 'api'}}
        result = self.helpers.get_project_specific_ignores(api_data)
        assert '*.db' in result