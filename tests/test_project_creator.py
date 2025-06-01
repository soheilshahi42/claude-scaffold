"""Comprehensive tests for ProjectCreator."""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import shutil
import subprocess

from src.core.project_creator import ProjectCreator


class TestProjectCreator:
    """Test cases for ProjectCreator."""
    
    @pytest.fixture
    def creator(self):
        """Create ProjectCreator instance with mocked dependencies."""
        with patch('src.core.project_creator.ProjectTemplates') as mock_templates, \
             patch('src.core.project_creator.InteractiveSetup') as mock_interactive, \
             patch('src.core.project_creator.DocumentationGenerator') as mock_doc_gen, \
             patch('src.core.project_creator.ProjectHelpers') as mock_helpers:
            
            creator = ProjectCreator()
            creator.templates = mock_templates.return_value
            creator.interactive_setup = mock_interactive.return_value
            creator.doc_generator = mock_doc_gen.return_value
            creator.helpers = mock_helpers.return_value
            
            yield creator
    
    def test_initialization(self):
        """Test ProjectCreator initialization."""
        with patch('src.core.project_creator.ProjectTemplates') as mock_templates, \
             patch('src.core.project_creator.InteractiveSetup') as mock_interactive, \
             patch('src.core.project_creator.DocumentationGenerator') as mock_doc_gen, \
             patch('src.core.project_creator.ProjectHelpers') as mock_helpers:
            
            creator = ProjectCreator()
            
            # Verify all components are initialized
            mock_templates.assert_called_once()
            mock_interactive.assert_called_once()
            mock_doc_gen.assert_called_once()
            mock_helpers.assert_called_once()
    
    @patch('subprocess.run')
    def test_check_claude_available_success(self, mock_run, creator):
        """Test Claude CLI availability check - success case."""
        mock_run.return_value.returncode = 0
        
        result = creator.check_claude_available()
        
        assert result is True
        mock_run.assert_called_once_with(['claude', '--version'], capture_output=True, text=True)
    
    @patch('subprocess.run')
    def test_check_claude_available_failure(self, mock_run, creator):
        """Test Claude CLI availability check - failure case."""
        mock_run.return_value.returncode = 1
        
        result = creator.check_claude_available()
        
        assert result is False
    
    @patch('subprocess.run')
    def test_check_claude_available_not_found(self, mock_run, creator):
        """Test Claude CLI availability check - command not found."""
        mock_run.side_effect = FileNotFoundError()
        
        result = creator.check_claude_available()
        
        assert result is False
    
    def test_create_project_already_exists_no_force(self, creator, temp_dir, capsys):
        """Test project creation when directory exists without force."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()
        
        result = creator.create_project("test_project", project_path, force=False)
        
        assert result is False
        captured = capsys.readouterr()
        assert "already exists" in captured.err
    
    def test_create_project_already_exists_with_force(self, creator, temp_dir, mock_project_data):
        """Test project creation when directory exists with force."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()
        (project_path / "old_file.txt").touch()
        
        creator.interactive_setup.run.return_value = mock_project_data
        creator.helpers.get_default_project_data.return_value = mock_project_data
        
        with patch.object(creator, '_create_directory_structure'), \
             patch.object(creator, '_create_claude_integration'), \
             patch.object(creator, '_init_git'):
            
            result = creator.create_project("test_project", project_path, force=True, interactive=False)
            
            assert result is True
            assert not (project_path / "old_file.txt").exists()
    
    def test_create_project_interactive_mode(self, creator, temp_dir, mock_project_data):
        """Test interactive project creation."""
        project_path = temp_dir / "test_project"
        
        creator.interactive_setup.run.return_value = mock_project_data
        creator.check_claude_available = Mock(return_value=True)
        
        with patch.object(creator, '_create_directory_structure') as mock_create_dirs, \
             patch.object(creator, '_create_claude_integration') as mock_claude_int, \
             patch.object(creator, '_init_git') as mock_init_git:
            
            result = creator.create_project("test_project", project_path, interactive=True)
            
            assert result is True
            creator.interactive_setup.run.assert_called_once_with("test_project", use_claude=True)
            mock_create_dirs.assert_called_once()
            creator.doc_generator.generate_documentation.assert_called_once()
            mock_claude_int.assert_called_once()
            mock_init_git.assert_called_once()
    
    def test_create_project_non_interactive_mode(self, creator, temp_dir, mock_project_data):
        """Test non-interactive project creation."""
        project_path = temp_dir / "test_project"
        
        creator.helpers.get_default_project_data.return_value = mock_project_data
        
        with patch.object(creator, '_create_directory_structure'), \
             patch.object(creator, '_create_claude_integration'), \
             patch.object(creator, '_init_git'):
            
            result = creator.create_project("test_project", project_path, interactive=False)
            
            assert result is True
            creator.helpers.get_default_project_data.assert_called_once_with("test_project")
            creator.interactive_setup.run.assert_not_called()
    
    def test_create_project_keyboard_interrupt(self, creator, temp_dir):
        """Test handling of keyboard interrupt during creation."""
        project_path = temp_dir / "test_project"
        
        creator.interactive_setup.run.side_effect = KeyboardInterrupt()
        
        result = creator.create_project("test_project", project_path)
        
        assert result is False
        assert not project_path.exists()
    
    def test_create_project_exception(self, creator, temp_dir, capsys):
        """Test handling of exceptions during creation."""
        project_path = temp_dir / "test_project"
        
        creator.interactive_setup.run.side_effect = Exception("Test error")
        
        result = creator.create_project("test_project", project_path)
        
        assert result is False
        captured = capsys.readouterr()
        assert "Test error" in captured.err
    
    def test_create_directory_structure(self, creator, temp_dir, mock_project_data):
        """Test directory structure creation."""
        project_path = temp_dir / "test_project"
        
        creator._create_directory_structure(project_path, mock_project_data)
        
        # Verify main directories
        assert project_path.exists()
        assert (project_path / "tests").exists()
        assert (project_path / "tests" / "__init__.py").exists()
        assert (project_path / ".claude").exists()
        assert (project_path / ".claude" / "commands").exists()
        
        # Verify module directories
        for module in mock_project_data['modules']:
            module_path = project_path / module['name']
            assert module_path.exists()
            assert (module_path / "__init__.py").exists()
            assert (module_path / "docs").exists()
            assert (module_path / "docs" / ".gitkeep").exists()
            
            # Verify test directories
            test_module_path = project_path / "tests" / module['name']
            assert test_module_path.exists()
            assert (test_module_path / "__init__.py").exists()
            assert (test_module_path / f"test_{module['name']}.py").exists()
    
    def test_create_directory_structure_web_project(self, creator, temp_dir, mock_project_data):
        """Test directory structure for web project type."""
        project_path = temp_dir / "test_project"
        mock_project_data['metadata']['project_type'] = 'web'
        
        creator._create_directory_structure(project_path, mock_project_data)
        
        assert (project_path / "static").exists()
        assert (project_path / "templates").exists()
    
    def test_create_directory_structure_ml_project(self, creator, temp_dir, mock_project_data):
        """Test directory structure for ML project type."""
        project_path = temp_dir / "test_project"
        mock_project_data['metadata']['project_type'] = 'ml'
        
        creator._create_directory_structure(project_path, mock_project_data)
        
        assert (project_path / "data").exists()
        assert (project_path / "models").exists()
        assert (project_path / "notebooks").exists()
    
    def test_create_claude_integration(self, creator, temp_dir, mock_project_data):
        """Test Claude integration setup."""
        project_path = temp_dir / "test_project"
        claude_path = project_path / ".claude"
        claude_path.mkdir(parents=True)
        commands_path = claude_path / "commands"
        commands_path.mkdir()
        
        creator.templates.get_template.return_value = "template content"
        creator.templates.create_custom_command.return_value = "#!/usr/bin/env python\n# command"
        creator.helpers.get_project_specific_ignores.return_value = "*.pyc\n__pycache__/"
        
        creator._create_claude_integration(project_path, mock_project_data)
        
        # Verify files created
        assert (claude_path / "settings.json").exists()
        assert (project_path / ".gitignore").exists()
        assert (project_path / "CLAUDE.local.md").exists()
        
        # Verify custom commands
        assert (commands_path / "test.py").exists()
        assert (commands_path / "build.py").exists()
        assert (commands_path / "test.py").stat().st_mode & 0o111  # Executable
    
    @patch('subprocess.run')
    def test_init_git_success(self, mock_run, creator, temp_dir, mock_project_data):
        """Test successful git initialization."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()
        
        mock_run.return_value.returncode = 0
        
        creator._init_git(project_path, mock_project_data)
        
        # Verify git commands called
        calls = mock_run.call_args_list
        assert len(calls) == 4
        assert calls[0] == call(['git', 'init'], cwd=project_path, check=True, capture_output=True)
        assert calls[1] == call(['git', 'checkout', '-b', 'main'], cwd=project_path, check=True, capture_output=True)
        assert calls[2] == call(['git', 'add', '.'], cwd=project_path, check=True, capture_output=True)
        assert 'Initial commit' in str(calls[3])
    
    @patch('subprocess.run')
    def test_init_git_failure(self, mock_run, creator, temp_dir, mock_project_data, capsys):
        """Test git initialization failure handling."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()
        
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        
        creator._init_git(project_path, mock_project_data)
        
        captured = capsys.readouterr()
        assert "Git initialization failed" in captured.out
    
    @patch('subprocess.run')
    def test_init_git_not_found(self, mock_run, creator, temp_dir, mock_project_data, capsys):
        """Test git command not found."""
        project_path = temp_dir / "test_project"
        project_path.mkdir()
        
        mock_run.side_effect = FileNotFoundError()
        
        creator._init_git(project_path, mock_project_data)
        
        captured = capsys.readouterr()
        assert "Git not found" in captured.out
    
    def test_create_project_without_git(self, creator, temp_dir, mock_project_data):
        """Test project creation without git initialization."""
        project_path = temp_dir / "test_project"
        mock_project_data['metadata']['git']['init'] = False
        
        creator.interactive_setup.run.return_value = mock_project_data
        
        with patch.object(creator, '_create_directory_structure'), \
             patch.object(creator, '_create_claude_integration'), \
             patch.object(creator, '_init_git') as mock_init_git:
            
            result = creator.create_project("test_project", project_path)
            
            assert result is True
            mock_init_git.assert_not_called()
    
    def test_create_project_default_path(self, creator, mock_project_data):
        """Test project creation with default path (current directory)."""
        creator.helpers.get_default_project_data.return_value = mock_project_data
        
        with patch('pathlib.Path.cwd') as mock_cwd, \
             patch.object(creator, '_create_directory_structure'), \
             patch.object(creator, '_create_claude_integration'), \
             patch.object(creator, '_init_git'):
            
            mock_cwd.return_value = Path("/current/dir")
            
            result = creator.create_project("test_project", interactive=False)
            
            assert result is True
            # Verify project path is current_dir / project_name
            creator._create_directory_structure.assert_called_once()
            args = creator._create_directory_structure.call_args[0]
            assert args[0] == Path("/current/dir/test_project")