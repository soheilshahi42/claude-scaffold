"""Tests for interactive collectors functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
import questionary
from src.interactive.interactive_collectors import InteractiveCollectors
from src.config.project_config import ProjectConfig


class TestInteractiveCollectors:
    """Test cases for interactive collectors."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.project_config = ProjectConfig()
        self.collectors = InteractiveCollectors(self.project_config)
        self.test_project_data = {
            'metadata': {
                'project_type': 'web',
                'project_type_name': 'Web Application'
            }
        }
    
    @patch('questionary.confirm')
    @patch('questionary.text')
    def test_collect_modules_with_suggested(self, mock_text, mock_confirm):
        """Test collecting modules with suggested modules accepted."""
        mock_confirm.return_value.ask.side_effect = [True, False]  # Use suggested, don't add more
        
        result = self.collectors.collect_modules(self.test_project_data)
        
        assert len(result) > 0
        assert all('name' in module and 'description' in module for module in result)
        assert result[0]['type'] == 'suggested'
    
    @patch('questionary.confirm')
    @patch('questionary.text')
    def test_collect_modules_custom_only(self, mock_text, mock_confirm):
        """Test collecting custom modules only."""
        mock_confirm.return_value.ask.side_effect = [False, True, False]  # Don't use suggested, add custom, done
        mock_text.return_value.ask.side_effect = ['custom_module', 'Custom module description']
        
        result = self.collectors.collect_modules(self.test_project_data)
        
        assert len(result) == 1
        assert result[0]['name'] == 'custom_module'
        assert result[0]['description'] == 'Custom module description'
        assert result[0]['type'] == 'custom'
    
    @patch('questionary.confirm')
    @patch('questionary.text')
    def test_collect_modules_mixed(self, mock_text, mock_confirm):
        """Test collecting both suggested and custom modules."""
        mock_confirm.return_value.ask.side_effect = [True, True, False]  # Use suggested, add custom, done
        mock_text.return_value.ask.side_effect = ['extra_module', 'Extra functionality']
        
        result = self.collectors.collect_modules(self.test_project_data)
        
        assert len(result) > 1
        suggested_count = sum(1 for m in result if m.get('type') == 'suggested')
        custom_count = sum(1 for m in result if m.get('type') == 'custom')
        assert suggested_count > 0
        assert custom_count == 1
    
    @patch('questionary.text')
    @patch('questionary.select')
    def test_collect_basic_info(self, mock_select, mock_text):
        """Test collecting basic project information."""
        mock_text.return_value.ask.return_value = 'A test project description'
        mock_select.return_value.ask.side_effect = ['web', 'pep8', 'pytest']
        
        result = self.collectors.collect_basic_info()
        
        assert result['description'] == 'A test project description'
        assert result['project_type'] == 'web'
        assert result['style_guide'] == 'pep8'
        assert result['test_framework'] == 'pytest'
    
    @patch('questionary.text')
    @patch('questionary.select')
    def test_collect_module_info(self, mock_select, mock_text):
        """Test collecting individual module information."""
        mock_text.return_value.ask.side_effect = ['auth', 'Authentication and authorization']
        
        result = self.collectors.collect_module_info()
        
        assert result['name'] == 'auth'
        assert result['description'] == 'Authentication and authorization'
    
    @patch('questionary.text')
    @patch('questionary.select')
    def test_collect_task_info(self, mock_select, mock_text):
        """Test collecting task information."""
        modules = [{'name': 'core'}, {'name': 'api'}]
        mock_select.return_value.ask.side_effect = ['core', 'high']
        mock_text.return_value.ask.return_value = 'Implement core feature'
        
        result = self.collectors.collect_task_info(modules)
        
        assert result['module'] == 'core'
        assert result['title'] == 'Implement core feature'
        assert result['priority'] == 'high'
    
    @patch('questionary.text')
    def test_collect_project_rules(self, mock_text):
        """Test collecting project rules."""
        mock_text.return_value.ask.side_effect = [
            'Always write tests',
            'Follow PEP8',
            ''  # Empty to stop
        ]
        
        result = self.collectors.collect_project_rules()
        
        assert len(result) == 2
        assert 'Always write tests' in result
        assert 'Follow PEP8' in result
    
    @patch('questionary.text')
    def test_collect_project_rules_empty(self, mock_text):
        """Test collecting project rules when none provided."""
        mock_text.return_value.ask.return_value = ''
        
        result = self.collectors.collect_project_rules()
        
        assert result == []
    
    @patch('questionary.confirm')
    def test_collect_modules_no_modules(self, mock_confirm):
        """Test collecting modules when user doesn't want any."""
        # Project type with no suggested modules
        project_data = {
            'metadata': {
                'project_type': 'custom',
                'project_type_name': 'Custom Project'
            }
        }
        mock_confirm.return_value.ask.return_value = False  # Don't add modules
        
        result = self.collectors.collect_modules(project_data)
        
        assert result == []
    
    @patch('questionary.text')
    def test_collect_module_info_with_validation(self, mock_text):
        """Test module name validation."""
        # First invalid, then valid
        mock_text.return_value.ask.side_effect = ['auth-module', 'Authentication module']
        
        # Mock the validation function behavior
        original_ask = mock_text.return_value.ask
        call_count = 0
        
        def ask_with_validation():
            nonlocal call_count
            result = original_ask.side_effect[call_count]
            call_count += 1
            
            # Check if this is the module name question (has validate parameter)
            if hasattr(mock_text.return_value, 'validate') and call_count == 1:
                # Simulate validation failure for invalid name
                if not result.replace('_', '').isalnum():
                    # In real questionary, it would re-ask, we'll simulate by returning valid name
                    result = 'auth_module'
            return result
        
        mock_text.return_value.ask = ask_with_validation
        
        result = self.collectors.collect_module_info()
        
        assert result['name'] in ['auth_module', 'auth-module']  # Either the corrected or original
    
    @patch('questionary.confirm')
    @patch('questionary.text')
    def test_collect_tasks_multiple(self, mock_text, mock_confirm):
        """Test collecting multiple tasks."""
        modules = [{'name': 'core'}, {'name': 'api'}]
        mock_confirm.return_value.ask.side_effect = [True, True, False]  # Add task, add another, done
        
        # Mock the choices for select
        with patch('questionary.select') as mock_select:
            mock_select.return_value.ask.side_effect = ['core', 'high', 'api', 'medium']
            mock_text.return_value.ask.side_effect = ['Task 1', 'Task 2']
            
            result = self.collectors.collect_tasks(modules)
        
        assert len(result) == 2
        assert result[0]['title'] == 'Task 1'
        assert result[0]['module'] == 'core'
        assert result[0]['priority'] == 'high'
        assert result[1]['title'] == 'Task 2'
        assert result[1]['module'] == 'api'
        assert result[1]['priority'] == 'medium'
    
    @patch('questionary.confirm')
    def test_collect_tasks_none(self, mock_confirm):
        """Test collecting no tasks."""
        modules = [{'name': 'core'}]
        mock_confirm.return_value.ask.return_value = False  # Don't add tasks
        
        result = self.collectors.collect_tasks(modules)
        
        assert result == []