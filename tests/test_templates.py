"""Comprehensive tests for template system."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.templates.templates import ProjectTemplates


class TestProjectTemplates:
    """Test cases for ProjectTemplates."""
    
    @pytest.fixture
    def templates(self):
        """Create ProjectTemplates instance."""
        return ProjectTemplates()
    
    def test_initialization(self):
        """Test ProjectTemplates initialization."""
        with patch('src.templates.templates.BaseTemplates') as mock_base, \
             patch('src.templates.templates.WorkflowTemplates') as mock_workflow, \
             patch('src.templates.templates.CommandTemplates') as mock_command, \
             patch('src.templates.templates.ProjectSpecificTemplates') as mock_project:
            
            mock_base.get_templates.return_value = {'base': 'template'}
            mock_workflow.get_templates.return_value = {'workflow': 'template'}
            mock_command.get_templates.return_value = {'command': 'template'}
            mock_project.get_templates.return_value = {'project': 'template'}
            
            templates = ProjectTemplates()
            
            assert templates.base_templates == {'base': 'template'}
            assert templates.workflow_templates == {'workflow': 'template'}
            assert templates.command_templates == {'command': 'template'}
            assert templates.project_templates == {'project': 'template'}
    
    def test_get_template_base(self, templates):
        """Test getting base template."""
        templates.base_templates = {
            'test_template': 'Hello {name}'
        }
        
        result = templates.get_template('test_template', {'name': 'World'})
        
        assert result == 'Hello World'
    
    def test_get_template_workflow(self, templates):
        """Test getting workflow template."""
        templates.workflow_templates = {
            'research_template': 'Research for {task_name}'
        }
        
        result = templates.get_template('research_template', {'task_name': 'API'})
        
        assert result == 'Research for API'
    
    def test_get_template_not_found(self, templates):
        """Test getting non-existent template."""
        with pytest.raises(ValueError) as exc_info:
            templates.get_template('non_existent', {})
        
        assert "Template 'non_existent' not found" in str(exc_info.value)
    
    def test_prepare_context_defaults(self, templates):
        """Test context preparation with defaults."""
        context = {}
        
        prepared = templates._prepare_context(context)
        
        assert 'timestamp' in prepared
        assert prepared['project_structure'] == 'Project structure will be generated'
        assert prepared['module_overview'] == 'Module overview will be generated'
        assert prepared['tasks_by_module'] == 'Tasks will be listed here'
        assert prepared['todo_items'] == '- [ ] No tasks defined yet'
        assert prepared['status_summary'] == '📊 0/0 tasks completed (0%)'
    
    def test_prepare_context_merge(self, templates):
        """Test context preparation with custom values."""
        context = {
            'project_name': 'test',
            'todo_items': '- [ ] Task 1\n- [ ] Task 2'
        }
        
        prepared = templates._prepare_context(context)
        
        assert prepared['project_name'] == 'test'
        assert prepared['todo_items'] == '- [ ] Task 1\n- [ ] Task 2'
        assert 'timestamp' in prepared  # Default still added
    
    def test_format_list_of_dicts_modules(self, templates):
        """Test formatting list of module dicts."""
        items = [
            {'name': 'api', 'description': 'API module'},
            {'name': 'auth', 'description': 'Authentication'}
        ]
        
        result = templates._format_list_of_dicts(items)
        
        assert '- **api**: API module' in result
        assert '- **auth**: Authentication' in result
    
    def test_format_list_of_dicts_tasks(self, templates):
        """Test formatting list of task dicts."""
        items = [
            {'title': 'Build API', 'module': 'api'},
            {'title': 'Add auth', 'module': 'auth'}
        ]
        
        result = templates._format_list_of_dicts(items)
        
        assert '- [api] Build API' in result
        assert '- [auth] Add auth' in result
    
    def test_format_list_of_dicts_empty(self, templates):
        """Test formatting empty list."""
        result = templates._format_list_of_dicts([])
        
        assert result == "None"
    
    def test_format_dict(self, templates):
        """Test dictionary formatting."""
        d = {
            'key1': 'value1',
            'key2': ['item1', 'item2']
        }
        
        result = templates._format_dict(d)
        
        assert '**key1**: value1' in result
        assert '**key2**:' in result
        assert '  - item1' in result
        assert '  - item2' in result
    
    def test_format_dict_empty(self, templates):
        """Test formatting empty dict."""
        result = templates._format_dict({})
        
        assert result == "None"
    
    def test_indent(self, templates):
        """Test text indentation."""
        text = "Line 1\nLine 2\nLine 3"
        
        result = templates._indent(text, 4)
        
        assert result == "    Line 1\n    Line 2\n    Line 3"
    
    def test_create_custom_command_test(self, templates):
        """Test creating test command."""
        templates.command_templates = {
            'test_command': '#!/usr/bin/env python\n# Test: {test_command}'
        }
        
        project_data = {
            'project_name': 'test',
            'metadata': {
                'commands': {
                    'test': 'pytest'
                }
            }
        }
        
        result = templates.create_custom_command('test', project_data)
        
        assert result == '#!/usr/bin/env python\n# Test: pytest'
    
    def test_create_custom_command_build(self, templates):
        """Test creating build command."""
        templates.command_templates = {
            'build_command': '# Build: {build_command}\n# Test: {test_command}'
        }
        
        project_data = {
            'project_name': 'test',
            'metadata': {
                'commands': {
                    'build': 'python setup.py build',
                    'test': 'pytest'
                }
            }
        }
        
        result = templates.create_custom_command('build', project_data)
        
        assert '# Build: python setup.py build' in result
        assert '# Test: pytest' in result
    
    def test_create_custom_command_not_found(self, templates):
        """Test creating command when not in metadata."""
        project_data = {
            'metadata': {
                'commands': {}
            }
        }
        
        result = templates.create_custom_command('test', project_data)
        
        assert result is None
    
    def test_complex_template_rendering(self, templates, sample_template_context):
        """Test rendering complex template with full context."""
        templates.base_templates = {
            'complex': '''Project: {project_name}
Description: {project_description}
Modules:
{module_overview}
Tasks by Module:
{tasks_by_module}
Rules:
{rules_list}'''
        }
        
        result = templates.get_template('complex', sample_template_context)
        
        assert 'Project: test_project' in result
        assert 'Description: A test project' in result
        assert '- **core**: Core functionality' in result
    
    def test_prepare_context_list_conversion(self, templates):
        """Test context preparation converts lists properly."""
        context = {
            'modules': [
                {'name': 'mod1', 'description': 'Module 1'},
                {'name': 'mod2', 'description': 'Module 2'}
            ],
            'rules': {
                'suggested': ['Rule 1', 'Rule 2']
            }
        }
        
        prepared = templates._prepare_context(context)
        
        # Lists of dicts should be formatted
        assert isinstance(prepared['modules'], str)
        assert '**mod1**' in prepared['modules']
        
        # Nested dicts should be formatted
        assert isinstance(prepared['rules'], str)
        assert '**suggested**' in prepared['rules']