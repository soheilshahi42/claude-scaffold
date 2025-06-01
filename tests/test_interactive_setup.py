"""Comprehensive tests for InteractiveSetup."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import yaml

from src.interactive.interactive_setup import InteractiveSetup


class TestInteractiveSetup:
    """Test cases for InteractiveSetup."""
    
    @pytest.fixture
    def setup(self):
        """Create InteractiveSetup instance with mocked dependencies."""
        with patch('src.interactive.interactive_setup.ProjectConfig') as mock_config, \
             patch('src.interactive.interactive_setup.InteractiveCollectors') as mock_collectors, \
             patch('src.interactive.interactive_setup.EnhancedClaudeInteractiveSetup') as mock_claude:
            
            setup = InteractiveSetup()
            setup.project_config = mock_config.return_value
            setup.collectors = mock_collectors.return_value
            
            # Set up mock project types
            setup.project_config.project_types = {
                'web': {
                    'name': 'Web Application',
                    'description': 'Full-stack web app'
                },
                'cli': {
                    'name': 'CLI Tool',
                    'description': 'Command-line tool'
                }
            }
            setup.project_config.style_guides = {
                'pep8': 'PEP 8',
                'black': 'Black'
            }
            setup.project_config.test_frameworks = {
                'pytest': 'pytest',
                'unittest': 'unittest'
            }
            
            yield setup
    
    @patch('subprocess.run')
    def test_check_claude_available_success(self, mock_run, setup):
        """Test Claude availability check - success."""
        mock_run.return_value.returncode = 0
        
        result = setup._check_claude_available()
        
        assert result is True
        mock_run.assert_called_once_with(['claude', '--version'], capture_output=True, text=True)
    
    @patch('subprocess.run')
    def test_check_claude_available_failure(self, mock_run, setup):
        """Test Claude availability check - failure."""
        mock_run.return_value.returncode = 1
        
        result = setup._check_claude_available()
        
        assert result is False
    
    @patch('subprocess.run')
    def test_check_claude_available_not_found(self, mock_run, setup):
        """Test Claude not found."""
        mock_run.side_effect = FileNotFoundError()
        
        result = setup._check_claude_available()
        
        assert result is False
    
    def test_run_with_claude_available(self, setup):
        """Test run with Claude available."""
        with patch.object(setup, '_check_claude_available', return_value=True), \
             patch('src.interactive.interactive_setup.EnhancedClaudeInteractiveSetup') as mock_claude:
            
            mock_claude_instance = mock_claude.return_value
            mock_claude_instance.run.return_value = {'project_name': 'test'}
            
            result = setup.run('test_project', use_claude=True)
            
            mock_claude_instance.run.assert_called_once_with('test_project', use_claude=True)
            assert result == {'project_name': 'test'}
    
    def test_run_without_claude(self, setup, mock_questionary):
        """Test run without Claude."""
        # Setup collectors
        setup.collectors.collect_modules.return_value = [
            {'name': 'core', 'description': 'Core module'}
        ]
        setup.collectors.collect_tasks.return_value = []
        setup.collectors.collect_rules.return_value = {'suggested': [], 'custom': []}
        setup.collectors.collect_additional_config.return_value = {
            'constraints': [],
            'metadata': {'commands': {}}
        }
        
        with patch.object(setup, '_check_claude_available', return_value=False), \
             patch.object(setup, '_collect_project_info') as mock_collect_info, \
             patch.object(setup, '_review_and_confirm', return_value=True):
            
            mock_collect_info.return_value = {
                'project_name': 'test_project',
                'metadata': {'project_type': 'web'}
            }
            
            result = setup.run('test_project', use_claude=True)
            
            assert result is not None
            assert 'modules' in result
            mock_collect_info.assert_called_once()
    
    def test_run_keyboard_interrupt(self, setup):
        """Test handling keyboard interrupt."""
        with patch.object(setup, '_check_claude_available', return_value=False), \
             patch.object(setup, '_collect_project_info', side_effect=KeyboardInterrupt):
            
            with pytest.raises(KeyboardInterrupt):
                setup.run('test_project')
    
    def test_run_exception(self, setup):
        """Test handling general exception."""
        with patch.object(setup, '_check_claude_available', return_value=False), \
             patch.object(setup, '_collect_project_info', side_effect=Exception("Test error")):
            
            with pytest.raises(Exception) as exc_info:
                setup.run('test_project')
            
            assert str(exc_info.value) == "Test error"
    
    def test_collect_project_info(self, setup, mock_questionary):
        """Test project info collection."""
        # Mock questionary responses
        mock_questionary['select'].return_value.ask.side_effect = [
            'web',  # project type
            'Python',  # language
            'pep8',  # style guide
        ]
        mock_questionary['text'].return_value.ask.return_value = 'A test project'
        mock_questionary['confirm'].return_value.ask.return_value = True
        
        project_data = {'project_name': 'test', 'metadata': {}}
        
        result = setup._collect_project_info(project_data)
        
        assert result['metadata']['project_type'] == 'web'
        assert result['metadata']['project_type_name'] == 'Web Application'
        assert result['metadata']['description'] == 'A test project'
        assert result['metadata']['language'] == 'Python'
        assert result['metadata']['style_guide'] == 'pep8'
        assert result['metadata']['test_framework'] == 'pytest'
    
    def test_collect_project_info_non_python(self, setup, mock_questionary):
        """Test project info collection for non-Python project."""
        mock_questionary['select'].return_value.ask.side_effect = [
            'web',  # project type
            'JavaScript',  # language
        ]
        mock_questionary['text'].return_value.ask.return_value = 'JS project'
        mock_questionary['confirm'].return_value.ask.return_value = True
        
        project_data = {'project_name': 'test', 'metadata': {}}
        
        result = setup._collect_project_info(project_data)
        
        assert result['metadata']['language'] == 'JavaScript'
        assert result['metadata']['style_guide'] == 'custom'
    
    def test_collect_project_info_custom_test_framework(self, setup, mock_questionary):
        """Test selecting custom test framework."""
        mock_questionary['select'].return_value.ask.side_effect = [
            'cli',  # project type
            'Python',  # language
            'black',  # style guide
            'unittest'  # test framework
        ]
        mock_questionary['text'].return_value.ask.return_value = 'CLI tool'
        mock_questionary['confirm'].return_value.ask.side_effect = [
            False,  # Don't use default test framework
            True    # Other confirms
        ]
        
        project_data = {'project_name': 'test', 'metadata': {}}
        setup.project_config.project_types['cli']['test_framework'] = 'pytest'
        
        result = setup._collect_project_info(project_data)
        
        assert result['metadata']['test_framework'] == 'unittest'
    
    def test_review_and_confirm_accepted(self, setup, mock_questionary):
        """Test review and confirm - accepted."""
        mock_questionary['confirm'].return_value.ask.return_value = True
        
        project_data = {
            'project_name': 'test',
            'modules': [{'name': 'core', 'description': 'Core', 'type': 'suggested'}],
            'tasks': [{'title': 'Task 1', 'module': 'core', 'priority': 'high'}],
            'rules': {'suggested': ['Rule 1'], 'custom': ['Custom rule']},
            'metadata': {
                'project_type_name': 'Web App',
                'description': 'Test description',
                'language': 'Python',
                'style_guide': 'pep8',
                'test_framework': 'pytest',
                'commands': {'test': 'pytest', 'build': 'python setup.py'}
            }
        }
        
        result = setup._review_and_confirm(project_data)
        
        assert result is True
    
    def test_review_and_confirm_rejected(self, setup, mock_questionary):
        """Test review and confirm - rejected."""
        mock_questionary['confirm'].return_value.ask.return_value = False
        
        project_data = {
            'project_name': 'test',
            'modules': [],
            'tasks': [],
            'rules': {'suggested': [], 'custom': []},
            'metadata': {
                'project_type_name': 'CLI',
                'description': 'CLI tool',
                'language': 'Python'
            }
        }
        
        result = setup._review_and_confirm(project_data)
        
        assert result is False
    
    def test_save_config(self, setup, temp_dir):
        """Test configuration saving."""
        project_data = {
            'project_name': 'test',
            'modules': [{'name': 'core'}],
            'metadata': {'type': 'web'}
        }
        
        config_path = temp_dir / '.claude'
        
        setup.save_config(project_data, temp_dir)
        
        # Verify file created
        assert (config_path / 'project_config.yaml').exists()
        
        # Verify content
        with open(config_path / 'project_config.yaml', 'r') as f:
            saved_data = yaml.safe_load(f)
        
        assert saved_data['project_name'] == 'test'
        assert saved_data['modules'][0]['name'] == 'core'
    
    def test_load_config_exists(self, setup, temp_dir):
        """Test loading existing configuration."""
        # Create config file
        config_path = temp_dir / '.claude'
        config_path.mkdir()
        
        test_data = {
            'project_name': 'test',
            'modules': [{'name': 'api'}]
        }
        
        with open(config_path / 'project_config.yaml', 'w') as f:
            yaml.dump(test_data, f)
        
        # Load config
        result = setup.load_config(temp_dir)
        
        assert result is not None
        assert result['project_name'] == 'test'
        assert result['modules'][0]['name'] == 'api'
    
    def test_load_config_not_exists(self, setup, temp_dir):
        """Test loading non-existent configuration."""
        result = setup.load_config(temp_dir)
        
        assert result is None
    
    def test_initialization(self):
        """Test InteractiveSetup initialization."""
        with patch('src.interactive.interactive_setup.ProjectConfig') as mock_config, \
             patch('src.interactive.interactive_setup.InteractiveCollectors') as mock_collectors:
            
            setup = InteractiveSetup()
            
            # Verify components initialized
            mock_config.assert_called_once()
            mock_collectors.assert_called_once_with(mock_config.return_value)
            
            # Verify backward compatibility properties
            assert hasattr(setup, 'project_types')
            assert hasattr(setup, 'style_guides')
            assert hasattr(setup, 'test_frameworks')
    
    def test_run_claude_disabled(self, setup, mock_questionary):
        """Test run with Claude explicitly disabled."""
        # Setup collectors
        setup.collectors.collect_modules.return_value = []
        setup.collectors.collect_tasks.return_value = []
        setup.collectors.collect_rules.return_value = {'suggested': [], 'custom': []}
        setup.collectors.collect_additional_config.return_value = {
            'constraints': [],
            'metadata': {'commands': {}}
        }
        
        with patch.object(setup, '_check_claude_available', return_value=True), \
             patch.object(setup, '_collect_project_info') as mock_collect_info, \
             patch.object(setup, '_review_and_confirm', return_value=True), \
             patch('src.interactive.interactive_setup.EnhancedClaudeInteractiveSetup') as mock_claude:
            
            mock_collect_info.return_value = {
                'project_name': 'test_project',
                'metadata': {}
            }
            
            result = setup.run('test_project', use_claude=False)
            
            # Should not use Claude even though it's available
            mock_claude.assert_not_called()
            assert result is not None
    
    def test_review_with_many_items(self, setup, mock_questionary):
        """Test review with many tasks and rules."""
        mock_questionary['confirm'].return_value.ask.return_value = True
        
        # Create many tasks
        tasks = [{'title': f'Task {i}', 'module': 'core', 'priority': 'medium'} 
                for i in range(10)]
        
        # Create many rules
        rules = {'suggested': [f'Rule {i}' for i in range(5)], 
                'custom': [f'Custom {i}' for i in range(3)]}
        
        project_data = {
            'project_name': 'test',
            'modules': [],
            'tasks': tasks,
            'rules': rules,
            'metadata': {
                'project_type_name': 'Web',
                'description': 'Test',
                'language': 'Python',
                'commands': {}
            }
        }
        
        result = setup._review_and_confirm(project_data)
        
        assert result is True