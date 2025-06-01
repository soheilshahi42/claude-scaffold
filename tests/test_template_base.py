"""Tests for base template functionality."""

import pytest
from src.templates.template_base import BaseTemplates


class TestBaseTemplates:
    """Test cases for base templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.base_templates = BaseTemplates()
    
    def test_get_templates_returns_dict(self):
        """Test that get_templates returns a dictionary."""
        templates = BaseTemplates.get_templates()
        
        assert isinstance(templates, dict)
        assert len(templates) > 0
    
    def test_get_templates_contains_required_templates(self):
        """Test that all required templates are present."""
        templates = BaseTemplates.get_templates()
        
        required_templates = [
            'root_claude',
            'readme',
            'global_rules',
            'tasks_md',
            'testing_md',
            'gitignore',
            'module_readme',
            'todo_md'
        ]
        
        for template_name in required_templates:
            assert template_name in templates
            assert isinstance(templates[template_name], str)
            assert len(templates[template_name]) > 0
    
    def test_root_claude_template_placeholders(self):
        """Test that root_claude template contains required placeholders."""
        templates = BaseTemplates.get_templates()
        root_claude = templates['root_claude']
        
        required_placeholders = [
            '{project_name}',
            '{description}',
            '{project_type}',
            '{language}',
            '{style_guide}',
            '{install_command}',
            '{test_command}',
            '{dev_command}',
            '{project_structure}',
            '{module_overview}'
        ]
        
        for placeholder in required_placeholders:
            assert placeholder in root_claude
    
    def test_readme_template_placeholders(self):
        """Test that readme template contains required placeholders."""
        templates = BaseTemplates.get_templates()
        readme = templates['readme']
        
        required_placeholders = [
            '{project_name}',
            '{description}',
            '{project_type}',
            '{language}',
            '{install_command}',
            '{test_command}',
            '{dev_command}'
        ]
        
        for placeholder in required_placeholders:
            assert placeholder in readme
    
    def test_global_rules_template_placeholders(self):
        """Test that global_rules template contains required placeholders."""
        templates = BaseTemplates.get_templates()
        global_rules = templates['global_rules']
        
        required_placeholders = [
            '{project_name}',
            '{style_guide}',
            '{project_rules}',
            '{language}'
        ]
        
        for placeholder in required_placeholders:
            assert placeholder in global_rules
    
    def test_tasks_md_template_placeholders(self):
        """Test that tasks_md template contains required placeholders."""
        templates = BaseTemplates.get_templates()
        tasks_md = templates['tasks_md']
        
        required_placeholders = [
            '{project_name}',
            '{task_list}',
            '{priority_counts}'
        ]
        
        for placeholder in required_placeholders:
            assert placeholder in tasks_md
    
    def test_module_readme_template_placeholders(self):
        """Test that module_readme template contains required placeholders."""
        templates = BaseTemplates.get_templates()
        module_readme = templates['module_readme']
        
        required_placeholders = [
            '{module_name_title}',
            '{module_description}',
            '{task_list}',
            '{testing_strategy}'
        ]
        
        for placeholder in required_placeholders:
            assert placeholder in module_readme
    
    def test_todo_md_template_placeholders(self):
        """Test that todo_md template contains required placeholders."""
        templates = BaseTemplates.get_templates()
        todo_md = templates['todo_md']
        
        required_placeholders = [
            '{project_name}',
            '{context}',
            '{todo_list}'
        ]
        
        for placeholder in required_placeholders:
            assert placeholder in todo_md
    
    def test_gitignore_template_content(self):
        """Test that gitignore template contains common patterns."""
        templates = BaseTemplates.get_templates()
        gitignore = templates['gitignore']
        
        common_patterns = [
            '__pycache__',
            '*.pyc',
            '.env',
            'venv/',
            '.pytest_cache',
            '.coverage',
            '*.log',
            '.DS_Store',
            'node_modules/',
            'dist/',
            'build/'
        ]
        
        for pattern in common_patterns:
            assert pattern in gitignore
    
    def test_testing_md_template_placeholders(self):
        """Test that testing_md template contains required placeholders."""
        templates = BaseTemplates.get_templates()
        testing_md = templates['testing_md']
        
        required_placeholders = [
            '{project_name}',
            '{test_framework}'
        ]
        
        for placeholder in required_placeholders:
            assert placeholder in testing_md
    
    def test_template_formatting(self):
        """Test that templates are properly formatted."""
        templates = BaseTemplates.get_templates()
        
        for name, template in templates.items():
            # Check for basic formatting
            assert not template.startswith('\n'), f"Template '{name}' should not start with newline"
            assert '{' in template and '}' in template, f"Template '{name}' should contain placeholders"
            
            # Check for markdown headers in documentation templates
            if name.endswith('_md') or name in ['root_claude', 'readme', 'global_rules']:
                assert '#' in template, f"Template '{name}' should contain markdown headers"
    
    def test_static_method_access(self):
        """Test that get_templates can be called as static method."""
        # Should work without instantiation
        templates = BaseTemplates.get_templates()
        assert isinstance(templates, dict)
        
        # Should also work with instance
        instance = BaseTemplates()
        templates_from_instance = instance.get_templates()
        assert templates == templates_from_instance