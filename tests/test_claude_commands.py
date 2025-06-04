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
        
        # Check for expected Markdown command files
        assert 'init-tasks.md' in templates
        assert 'dev.md' in templates
        assert 'test.md' in templates
        assert 'status.md' in templates
        assert 'review.md' in templates
        assert 'research.md' in templates
        
        # Check content is Markdown with instructions
        assert 'Initialize and review the task list' in templates['init-tasks.md']
        assert 'Start or resume development' in templates['dev.md']
    
    def test_init_tasks_command_content(self):
        """Test init-tasks command has expected instructions."""
        templates = CommandTemplates.get_templates()
        init_tasks = templates['init-tasks.md']
        
        # Check for key instructions
        assert 'read through CLAUDE.md' in init_tasks
        assert 'read TASKS.md' in init_tasks
        assert 'use the TodoWrite tool' in init_tasks
        assert 'provide a summary showing' in init_tasks
    
    def test_dev_command_content(self):
        """Test dev command has expected instructions."""
        templates = CommandTemplates.get_templates()
        dev_cmd = templates['dev.md']
        
        # Check for key instructions
        assert 'use TodoRead' in dev_cmd
        assert 'Read CLAUDE.md' in dev_cmd
        assert 'Read GLOBAL_RULES.md' in dev_cmd
        assert 'TDD workflow' in dev_cmd
        assert '$ARGUMENTS' in dev_cmd
    
    def test_commands_have_arguments_placeholder(self):
        """Test that commands support arguments where needed."""
        templates = CommandTemplates.get_templates()
        
        # Commands that should have $ARGUMENTS
        assert '$ARGUMENTS' in templates['dev.md']
        assert '$ARGUMENTS' in templates['status.md']
        assert '$ARGUMENTS' in templates['review.md']
        assert '$ARGUMENTS' in templates['research.md']
    
    def test_project_creator_generates_commands(self):
        """Test that project creator generates command files correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir) / "test_project"
            project_data = {
                "project_name": "test_project",
                "metadata": {
                    "commands": {
                        "test": "pytest"
                    }
                }
            }
            
            creator = ProjectCreator()
            creator._create_directory_structure(project_path, project_data)
            creator._create_claude_integration(project_path, project_data)
            
            # Check command files exist
            commands_dir = project_path / ".claude" / "commands"
            assert commands_dir.exists()
            
            # Check all command files are created
            assert (commands_dir / "init-tasks.md").exists()
            assert (commands_dir / "dev.md").exists()
            assert (commands_dir / "test.md").exists()
            assert (commands_dir / "status.md").exists()
            assert (commands_dir / "review.md").exists()
            assert (commands_dir / "research.md").exists()
            
            # Check test command has the test command replaced
            test_content = (commands_dir / "test.md").read_text()
            assert "pytest" in test_content