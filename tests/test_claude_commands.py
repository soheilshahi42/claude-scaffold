"""Tests for Claude Code command templates."""
import tempfile
from pathlib import Path
import pytest

from src.templates.template_commands import CommandTemplates
from src.core.project_creator import ProjectCreator


class TestClaudeCommands:
    """Test Claude Code command generation."""
    
    def test_command_templates_exist(self):
        """Test that Claude command templates are defined."""
        templates = CommandTemplates.get_templates()
        
        assert 'claude_init_tasks' in templates
        assert 'claude_dev_resume' in templates
        
        # Check content is valid Python
        assert '#!/usr/bin/env python3' in templates['claude_init_tasks']
        assert '#!/usr/bin/env python3' in templates['claude_dev_resume']
        
        # Check main functions exist
        assert 'def main():' in templates['claude_init_tasks']
        assert 'def main():' in templates['claude_dev_resume']
    
    def test_init_tasks_command_content(self):
        """Test init-tasks command has expected functionality."""
        templates = CommandTemplates.get_templates()
        init_tasks = templates['claude_init_tasks']
        
        # Check for key functions
        assert 'def parse_claude_md():' in init_tasks
        assert 'def create_todo_list(' in init_tasks
        
        # Check for expected file operations
        assert 'Path("CLAUDE.md")' in init_tasks
        assert 'Path("TASKS.md")' in init_tasks
        
        # Check for task parsing logic
        assert 'modules[module_name]' in init_tasks
        assert 'priority_map' in init_tasks
    
    def test_dev_resume_command_content(self):
        """Test dev resume command has expected functionality."""
        templates = CommandTemplates.get_templates()
        dev_resume = templates['claude_dev_resume']
        
        # Check for key functions
        assert 'def check_claude_installed():' in dev_resume
        assert 'def get_project_context():' in dev_resume
        assert 'def create_startup_prompt():' in dev_resume
        
        # Check for Claude CLI integration
        assert '["claude", "--version"]' in dev_resume
        assert 'subprocess.run(["claude", prompt]' in dev_resume
    
    def test_commands_created_in_project(self):
        """Test that commands are created when generating a project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            creator = ProjectCreator(debug_mode=True)
            
            # Create minimal project data
            project_data = {
                'project_name': 'test_project',
                'description': 'Test project',
                'metadata': {
                    'project_type': 'python',
                    'language': 'python',
                    'style_guide': 'PEP8',
                    'commands': {
                        'install': 'pip install -r requirements.txt',
                        'test': 'pytest',
                        'dev': 'python -m app'
                    },
                    'git': {'init': False}
                },
                'modules': [
                    {
                        'name': 'core',
                        'description': 'Core functionality',
                        'responsibilities': ['Main logic']
                    }
                ],
                'tasks': []
            }
            
            # Create project
            project_path = Path(tmpdir) / 'test_project'
            creator._create_directory_structure(project_path, project_data)
            creator._create_claude_integration(project_path, project_data)
            
            # Check commands were created
            commands_path = project_path / '.claude' / 'commands'
            assert commands_path.exists()
            
            # Check our new commands exist
            init_tasks_file = commands_path / 'init-tasks.py'
            dev_file = commands_path / 'dev.py'
            
            assert init_tasks_file.exists()
            assert dev_file.exists()
            
            # Check files are executable
            import os
            assert os.access(init_tasks_file, os.X_OK)
            assert os.access(dev_file, os.X_OK)
            
            # Check content
            init_content = init_tasks_file.read_text()
            assert '#!/usr/bin/env python3' in init_content
            assert 'parse_claude_md' in init_content
            
            dev_content = dev_file.read_text()
            assert '#!/usr/bin/env python3' in dev_content
            assert 'check_claude_installed' in dev_content