"""Tests for template system."""

import pytest
from src.templates import ProjectTemplates


class TestProjectTemplates:
    """Test cases for project templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.templates = ProjectTemplates()
    
    def test_templates_loaded(self):
        """Test that all template categories are loaded."""
        assert hasattr(self.templates, 'base_templates')
        assert hasattr(self.templates, 'workflow_templates')
        assert hasattr(self.templates, 'command_templates')
        assert hasattr(self.templates, 'project_templates')
    
    def test_get_base_template(self):
        """Test getting a base template."""
        context = {
            'project_name': 'test_project',
            'description': 'Test description',
            'project_type': 'Test Type',
            'language': 'Python',
            'style_guide': 'PEP 8'
        }
        
        result = self.templates.get_template('root_claude', context)
        
        assert 'test_project' in result
        assert 'Test description' in result
        assert 'Test Type' in result
        assert 'Python' in result
    
    def test_get_workflow_template(self):
        """Test getting a workflow template."""
        context = {
            'task_name': 'Test Task',
            'research_objective': 'Test objective',
            'key_questions': 'Question 1\nQuestion 2',
            'findings': 'Test findings',
            'recommendations': 'Test recommendations',
            'references': 'Test references',
            'next_steps': 'Next steps'
        }
        
        result = self.templates.get_template('research_template', context)
        
        assert 'Test Task' in result
        assert 'Test objective' in result
        assert 'Question 1' in result
    
    def test_get_command_template(self):
        """Test getting a command template."""
        context = {
            'test_command': 'pytest',
            'project_name': 'test_project'
        }
        
        result = self.templates.get_template('test_command', context)
        
        assert '#!/usr/bin/env python3' in result
        assert 'pytest' in result
        assert 'test_project' in result
    
    def test_get_project_template(self):
        """Test getting a project-specific template."""
        context = {
            'project_specific_ignores': '*.log\n*.tmp'
        }
        
        result = self.templates.get_template('gitignore', context)
        
        assert '# Python' in result
        assert '__pycache__/' in result
        assert '*.log' in result
        assert '*.tmp' in result
    
    def test_template_not_found(self):
        """Test error when template not found."""
        with pytest.raises(ValueError, match="Template 'nonexistent' not found"):
            self.templates.get_template('nonexistent', {})
    
    def test_prepare_context_defaults(self):
        """Test context preparation with defaults."""
        context = {'project_name': 'test'}
        prepared = self.templates._prepare_context(context)
        
        assert 'timestamp' in prepared
        assert 'project_structure' in prepared
        assert 'module_overview' in prepared
        assert prepared['todo_items'] == '- [ ] No tasks defined yet'
    
    def test_format_list_of_dicts(self):
        """Test formatting list of dictionaries."""
        items = [
            {'name': 'module1', 'description': 'Module 1 description'},
            {'title': 'Task 1', 'module': 'core'}
        ]
        
        result = self.templates._format_list_of_dicts(items)
        
        assert '- **module1**: Module 1 description' in result
        assert '- [core] Task 1' in result
    
    def test_create_custom_command_test(self):
        """Test creating custom test command."""
        project_data = {
            'project_name': 'test_project',
            'metadata': {
                'commands': {
                    'test': 'pytest --cov'
                }
            }
        }
        
        result = self.templates.create_custom_command('test', project_data)
        
        assert result is not None
        assert 'pytest --cov' in result
        assert 'test_project' in result
    
    def test_create_custom_command_none(self):
        """Test creating custom command when not defined."""
        project_data = {
            'metadata': {
                'commands': {}
            }
        }
        
        result = self.templates.create_custom_command('test', project_data)
        
        assert result is None