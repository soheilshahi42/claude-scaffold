"""Tests for project helpers functionality."""

import pytest
import yaml
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, mock_open
from src.utils.project_helpers import ProjectHelpers


class TestProjectHelpers:
    """Test cases for project helpers."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.helpers = ProjectHelpers()
        self.test_project_name = "test_project"
    
    def test_get_default_project_data(self):
        """Test getting default project data."""
        result = self.helpers.get_default_project_data(self.test_project_name)
        
        assert result['project_name'] == self.test_project_name
        assert 'timestamp' in result
        assert result['version'] == '0.1.0'
        assert len(result['modules']) == 1
        assert result['modules'][0]['name'] == 'core'
        assert result['tasks'] == []
        assert 'suggested' in result['rules']
        assert 'custom' in result['rules']
        assert result['metadata']['project_type'] == 'custom'
        assert result['metadata']['language'] == 'Python'
    
    def test_prepare_template_context_basic(self):
        """Test preparing basic template context."""
        project_data = {
            'project_name': 'test_project',
            'metadata': {
                'description': 'Test description',
                'project_type': 'web',
                'project_type_name': 'Web Application',
                'language': 'Python',
                'style_guide': 'pep8',
                'commands': {
                    'install': 'pip install -e .',
                    'test': 'pytest',
                    'dev': 'python app.py'
                }
            },
            'modules': [
                {'name': 'core', 'description': 'Core module'}
            ],
            'tasks': [
                {'priority': 'high'},
                {'priority': 'medium'},
                {'priority': 'medium'}
            ],
            'rules': {
                'suggested': ['Rule 1'],
                'custom': ['Custom rule']
            }
        }
        
        result = self.helpers.prepare_template_context(project_data)
        
        assert result['project_name'] == 'test_project'
        assert result['description'] == 'Test description'
        assert result['project_type'] == 'web'
        assert result['language'] == 'Python'
        assert result['style_guide'] == 'pep8'
        assert result['install_command'] == 'pip install -e .'
        assert result['test_command'] == 'pytest'
        assert result['dev_command'] == 'python app.py'
    
    def test_prepare_template_context_task_counts(self):
        """Test task counting in template context."""
        project_data = {
            'project_name': 'test',
            'metadata': {},
            'modules': [],
            'tasks': [
                {'priority': 'high'},
                {'priority': 'high'},
                {'priority': 'medium'},
                {'priority': 'low'},
                {'priority': 'unknown'}  # Should be counted as low
            ],
            'rules': {'suggested': [], 'custom': []}
        }
        
        result = self.helpers.prepare_template_context(project_data)
        
        assert 'High: 2' in result['priority_counts']
        assert 'Medium: 1' in result['priority_counts']
        assert 'Low: 1' in result['priority_counts']
    
    def test_prepare_template_context_module_overview(self):
        """Test module overview generation."""
        project_data = {
            'project_name': 'test',
            'metadata': {},
            'modules': [
                {'name': 'auth', 'description': 'Authentication module'},
                {'name': 'api', 'description': 'API endpoints'}
            ],
            'tasks': [],
            'rules': {'suggested': [], 'custom': []}
        }
        
        result = self.helpers.prepare_template_context(project_data)
        
        assert '### Auth' in result['module_overview']
        assert 'Authentication module' in result['module_overview']
        assert '### Api' in result['module_overview']
        assert 'API endpoints' in result['module_overview']
    
    def test_prepare_template_context_project_rules(self):
        """Test project rules formatting."""
        project_data = {
            'project_name': 'test',
            'metadata': {},
            'modules': [],
            'tasks': [],
            'rules': {
                'suggested': ['Rule 1', 'Rule 2'],
                'custom': ['Custom 1', 'Custom 2']
            }
        }
        
        result = self.helpers.prepare_template_context(project_data)
        
        assert '- Rule 1' in result['project_rules']
        assert '- Rule 2' in result['project_rules']
        assert '- Custom 1' in result['project_rules']
        assert '- Custom 2' in result['project_rules']
    
    def test_prepare_template_context_missing_metadata(self):
        """Test context preparation with missing metadata."""
        project_data = {
            'project_name': 'test',
            'modules': [],
            'tasks': [],
            'rules': {'suggested': [], 'custom': []}
        }
        
        result = self.helpers.prepare_template_context(project_data)
        
        # Should have defaults
        assert result['description'] == 'test project'
        assert result['project_type'] == 'general'
        assert result['language'] == 'Python'
        assert result['style_guide'] == 'pep8'
    
    @patch('pathlib.Path.write_text')
    @patch('yaml.dump')
    def test_save_config_success(self, mock_yaml_dump, mock_write):
        """Test saving configuration successfully."""
        config = {'project_name': 'test'}
        project_path = Path('/test/project')
        mock_yaml_dump.return_value = 'yaml content'
        
        self.helpers.save_config(project_path, config)
        
        expected_path = project_path / '.claude-scaffold.yml'
        mock_yaml_dump.assert_called_once()
        mock_write.assert_called_once()
    
    @patch('pathlib.Path.write_text')
    def test_save_config_error(self, mock_write):
        """Test saving configuration with error."""
        mock_write.side_effect = OSError("Permission denied")
        config = {'project_name': 'test'}
        project_path = Path('/test/project')
        
        # Should not raise exception
        self.helpers.save_config(project_path, config)
    
    def test_print_success_message(self, capsys):
        """Test printing success message."""
        project_path = Path('/test/project')
        config = {
            'modules': [{'name': 'core'}, {'name': 'api'}],
            'tasks': [1, 2, 3]  # Just need length
        }
        
        self.helpers.print_success_message(project_path, config)
        
        captured = capsys.readouterr()
        assert '✅ Project created successfully!' in captured.out
        assert str(project_path) in captured.out
        assert '2 modules' in captured.out
        assert '3 tasks' in captured.out
        assert 'Next steps:' in captured.out
    
    def test_generate_project_structure(self):
        """Test generating project structure."""
        modules = [
            {'name': 'core', 'description': 'Core module'},
            {'name': 'api', 'description': 'API module'}
        ]
        
        result = self.helpers.generate_project_structure('test_project', modules)
        
        assert 'test_project/' in result
        assert 'CLAUDE.md' in result
        assert 'docs/' in result
        assert 'core/' in result
        assert 'api/' in result
        assert 'README.md' in result
        assert 'TASKS.md' in result
    
    def test_generate_project_structure_no_modules(self):
        """Test generating project structure with no modules."""
        result = self.helpers.generate_project_structure('test_project', [])
        
        assert 'test_project/' in result
        assert 'CLAUDE.md' in result
        assert 'docs/' in result
        assert '└── modules/' not in result
    
    def test_format_task_list(self):
        """Test formatting task list."""
        tasks = [
            {'title': 'Task 1', 'priority': 'high', 'module': 'core'},
            {'title': 'Task 2', 'priority': 'medium', 'module': 'api'}
        ]
        
        result = self.helpers.formatters.format_task_list(tasks)
        
        assert '[HIGH] Task 1 (core)' in result
        assert '[MEDIUM] Task 2 (api)' in result
    
    def test_format_task_list_empty(self):
        """Test formatting empty task list."""
        result = self.helpers.formatters.format_task_list([])
        
        assert 'No tasks defined yet' in result
    
    def test_prepare_template_context_project_structure(self):
        """Test project structure in template context."""
        project_data = {
            'project_name': 'myproject',
            'metadata': {},
            'modules': [{'name': 'utils'}],
            'tasks': [],
            'rules': {'suggested': [], 'custom': []}
        }
        
        result = self.helpers.prepare_template_context(project_data)
        
        assert 'myproject/' in result['project_structure']
        assert 'utils/' in result['project_structure']