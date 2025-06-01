"""Tests for command template functionality."""

import pytest
from src.templates.template_commands import CommandTemplates


class TestCommandTemplates:
    """Test cases for command templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.command_templates = CommandTemplates()
    
    def test_get_templates_returns_dict(self):
        """Test that get_templates returns a dictionary."""
        templates = CommandTemplates.get_templates()
        
        assert isinstance(templates, dict)
        assert len(templates) > 0
    
    def test_get_templates_contains_required_templates(self):
        """Test that all required templates are present."""
        templates = CommandTemplates.get_templates()
        
        required_templates = [
            'test_command',
            'lint_command',
            'format_command',
            'dev_command',
            'build_command',
            'deploy_command'
        ]
        
        for template_name in required_templates:
            assert template_name in templates
            assert isinstance(templates[template_name], str)
            assert len(templates[template_name]) > 0
    
    def test_test_command_template_content(self):
        """Test that test command template has required content."""
        templates = CommandTemplates.get_templates()
        test_command = templates['test_command']
        
        # Check for required elements
        assert '#!/usr/bin/env python3' in test_command
        assert 'import subprocess' in test_command
        assert 'import sys' in test_command
        assert 'def main():' in test_command
        assert '{test_command}' in test_command
        assert '{project_name}' in test_command
        assert 'subprocess.run' in test_command
    
    def test_lint_command_template_content(self):
        """Test that lint command template has required content."""
        templates = CommandTemplates.get_templates()
        lint_command = templates['lint_command']
        
        # Check for required elements
        assert '#!/usr/bin/env python3' in lint_command
        assert 'import subprocess' in lint_command
        assert 'def main():' in lint_command
        assert 'lint' in lint_command.lower()
    
    def test_format_command_template_content(self):
        """Test that format command template has required content."""
        templates = CommandTemplates.get_templates()
        format_command = templates['format_command']
        
        # Check for required elements
        assert '#!/usr/bin/env python3' in format_command
        assert 'import subprocess' in format_command
        assert 'def main():' in format_command
        assert 'format' in format_command.lower()
    
    def test_dev_command_template_placeholders(self):
        """Test that dev command template contains required placeholders."""
        templates = CommandTemplates.get_templates()
        dev_command = templates['dev_command']
        
        # Should have placeholders for customization
        assert '{' in dev_command and '}' in dev_command
        
        # Check for development-related content
        assert 'dev' in dev_command.lower() or 'development' in dev_command.lower()
    
    def test_build_command_template_content(self):
        """Test that build command template has required content."""
        templates = CommandTemplates.get_templates()
        build_command = templates['build_command']
        
        # Check for build-related content
        assert 'build' in build_command.lower()
        assert '#!/usr/bin/env python3' in build_command
    
    def test_deploy_command_template_content(self):
        """Test that deploy command template has required content."""
        templates = CommandTemplates.get_templates()
        deploy_command = templates['deploy_command']
        
        # Check for deployment-related content
        assert 'deploy' in deploy_command.lower()
        assert '#!/usr/bin/env python3' in deploy_command
    
    def test_all_templates_are_executable_scripts(self):
        """Test that all templates start with shebang."""
        templates = CommandTemplates.get_templates()
        
        for name, template in templates.items():
            assert template.strip().startswith('#!/usr/bin/env python3'), \
                f"Template '{name}' should start with Python shebang"
    
    def test_all_templates_have_main_function(self):
        """Test that all templates have a main function."""
        templates = CommandTemplates.get_templates()
        
        for name, template in templates.items():
            assert 'def main():' in template, \
                f"Template '{name}' should have a main function"
    
    def test_static_method_access(self):
        """Test that get_templates can be called as static method."""
        # Should work without instantiation
        templates = CommandTemplates.get_templates()
        assert isinstance(templates, dict)
        
        # Should also work with instance
        instance = CommandTemplates()
        templates_from_instance = instance.get_templates()
        assert templates == templates_from_instance
    
    def test_template_subprocess_usage(self):
        """Test that templates use subprocess correctly."""
        templates = CommandTemplates.get_templates()
        
        for name, template in templates.items():
            if 'subprocess' in template:
                # Should import subprocess
                assert 'import subprocess' in template
                # Should use subprocess.run or subprocess.call
                assert 'subprocess.run' in template or 'subprocess.call' in template