"""Comprehensive tests for CLI module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import argparse
from pathlib import Path

from src.cli import main, print_banner


class TestCLI:
    """Test cases for CLI functionality."""
    
    def test_print_banner(self, capsys):
        """Test banner printing."""
        print_banner()
        
        captured = capsys.readouterr()
        assert "CLAUDE SCAFFOLD" in captured.out
        assert "Generate self-documenting Claude Code project skeletons" in captured.out
    
    @patch('src.cli.argparse.ArgumentParser.parse_args')
    @patch('src.cli.ClaudeScaffold')
    def test_main_no_command(self, mock_scaffold, mock_parse_args, capsys):
        """Test main with no command."""
        mock_parse_args.return_value = argparse.Namespace(command=None)
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "CLAUDE SCAFFOLD" in captured.out  # Banner printed
    
    @patch('sys.argv', ['claude-scaffold', 'new', 'test_project'])
    @patch('src.cli.ClaudeScaffold')
    def test_main_new_command_success(self, mock_scaffold_class):
        """Test new command - success."""
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.create_project.return_value = True
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        mock_scaffold.create_project.assert_called_once_with(
            project_name='test_project',
            project_path=None,
            force=False,
            interactive=True
        )
    
    @patch('sys.argv', ['claude-scaffold', 'new', 'test_project', '--path', '/custom/path'])
    @patch('src.cli.ClaudeScaffold')
    def test_main_new_with_custom_path(self, mock_scaffold_class):
        """Test new command with custom path."""
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.create_project.return_value = True
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        call_args = mock_scaffold.create_project.call_args
        assert call_args[1]['project_path'] == Path('/custom/path')
    
    @patch('sys.argv', ['claude-scaffold', 'new', 'test_project', '--force'])
    @patch('src.cli.ClaudeScaffold')
    def test_main_new_with_force(self, mock_scaffold_class):
        """Test new command with force flag."""
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.create_project.return_value = True
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        mock_scaffold.create_project.assert_called_once_with(
            project_name='test_project',
            project_path=None,
            force=True,
            interactive=True
        )
    
    @patch('sys.argv', ['claude-scaffold', 'new', 'test_project', '--no-interactive'])
    @patch('src.cli.ClaudeScaffold')
    def test_main_new_non_interactive(self, mock_scaffold_class, capsys):
        """Test new command in non-interactive mode."""
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.create_project.return_value = True
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        mock_scaffold.create_project.assert_called_once_with(
            project_name='test_project',
            project_path=None,
            force=False,
            interactive=False
        )
        
        # Banner should not be printed in non-interactive mode
        captured = capsys.readouterr()
        assert "CLAUDE SCAFFOLD" not in captured.out
    
    @patch('sys.argv', ['claude-scaffold', 'new', 'test_project'])
    @patch('src.cli.ClaudeScaffold')
    def test_main_new_command_failure(self, mock_scaffold_class):
        """Test new command - failure."""
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.create_project.return_value = False
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
    
    @patch('sys.argv', ['claude-scaffold', 'add-task', '.', 'api', 'Create endpoints'])
    @patch('src.cli.ClaudeScaffold')
    @patch('pathlib.Path.resolve')
    def test_main_add_task_success(self, mock_resolve, mock_scaffold_class):
        """Test add-task command - success."""
        mock_resolve.return_value = Path('/current/project')
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.add_task.return_value = True
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        mock_scaffold.add_task.assert_called_once_with(
            project_path=Path('/current/project'),
            module_name='api',
            task_title='Create endpoints',
            priority='medium'
        )
    
    @patch('sys.argv', ['claude-scaffold', 'add-task', '/project', 'backend', 'Add auth', '--priority', 'high'])
    @patch('src.cli.ClaudeScaffold')
    @patch('pathlib.Path.resolve')
    def test_main_add_task_with_priority(self, mock_resolve, mock_scaffold_class):
        """Test add-task command with priority."""
        mock_resolve.return_value = Path('/project')
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.add_task.return_value = True
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        mock_scaffold.add_task.assert_called_once_with(
            project_path=Path('/project'),
            module_name='backend',
            task_title='Add auth',
            priority='high'
        )
    
    @patch('sys.argv', ['claude-scaffold', 'add-task', '.', 'api', 'Task'])
    @patch('src.cli.ClaudeScaffold')
    def test_main_add_task_failure(self, mock_scaffold_class):
        """Test add-task command - failure."""
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.add_task.return_value = False
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
    
    @patch('sys.argv', ['claude-scaffold', 'new', 'test_project'])
    @patch('src.cli.ClaudeScaffold')
    def test_main_keyboard_interrupt(self, mock_scaffold_class, capsys):
        """Test handling keyboard interrupt."""
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.create_project.side_effect = KeyboardInterrupt()
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Operation cancelled by user" in captured.out
    
    @patch('sys.argv', ['claude-scaffold', 'new', 'test_project'])
    @patch('src.cli.ClaudeScaffold')
    def test_main_unexpected_exception(self, mock_scaffold_class, capsys):
        """Test handling unexpected exception."""
        mock_scaffold = mock_scaffold_class.return_value
        mock_scaffold.create_project.side_effect = Exception("Unexpected error")
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Unexpected error" in captured.err
    
    @patch('sys.argv', ['claude-scaffold', '--version'])
    def test_main_version(self, capsys):
        """Test version flag."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "0.1.0" in captured.out
    
    @patch('sys.argv', ['claude-scaffold', '--help'])
    def test_main_help(self, capsys):
        """Test help flag."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Claude Scaffold" in captured.out
        assert "Commands:" in captured.out
        assert "new" in captured.out
        assert "add-task" in captured.out
    
    @patch('sys.argv', ['claude-scaffold', 'new', '--help'])
    def test_main_new_help(self, capsys):
        """Test new command help."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Create a new Claude-ready project" in captured.out
        assert "--force" in captured.out
        assert "--no-interactive" in captured.out
    
    @patch('sys.argv', ['claude-scaffold', 'add-task', '--help'])
    def test_main_add_task_help(self, capsys):
        """Test add-task command help."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Add a task to an existing project" in captured.out
        assert "--priority" in captured.out
    
    def test_main_callable(self):
        """Test that main is callable."""
        assert callable(main)
    
    @patch('sys.argv', ['claude-scaffold', 'invalid-command'])
    def test_main_invalid_command(self, capsys):
        """Test invalid command."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        # argparse exits with code 2 for invalid arguments
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "invalid choice" in captured.err
    
    @patch('sys.argv', ['claude-scaffold', 'new'])
    def test_main_new_missing_project_name(self, capsys):
        """Test new command without project name."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "required" in captured.err.lower()
    
    @patch('sys.argv', ['claude-scaffold', 'add-task'])
    def test_main_add_task_missing_args(self, capsys):
        """Test add-task command without required arguments."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "required" in captured.err.lower()