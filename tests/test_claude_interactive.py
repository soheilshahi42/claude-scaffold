"""Tests for Claude interactive functionality."""

import pytest
import json
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock, call
from src.claude.claude_interactive import ClaudeInteractiveSetup


class TestClaudeInteractiveSetup:
    """Test cases for Claude interactive setup."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.claude_setup = ClaudeInteractiveSetup()
        self.test_project_name = "test_project"
    
    @patch('questionary.confirm')
    def test_run_with_claude_declined(self, mock_confirm):
        """Test run when user declines Claude enhancement."""
        mock_confirm.return_value.ask.return_value = False
        
        # Mock all collection methods
        self.claude_setup._collect_project_type = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_description = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_language = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_modules = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_tasks = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_rules = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_style_guide = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_test_framework = Mock(return_value={'project_name': 'test'})
        self.claude_setup._finalize_project_data = Mock(return_value={'project_name': 'test'})
        
        result = self.claude_setup.run(self.test_project_name)
        
        assert result['project_name'] == 'test'
        assert self.claude_setup._collect_project_type.call_args[0][1] is False
    
    @patch('questionary.confirm')
    def test_run_with_claude_accepted(self, mock_confirm):
        """Test run when user accepts Claude enhancement."""
        mock_confirm.return_value.ask.return_value = True
        
        # Mock all collection methods
        self.claude_setup._collect_project_type = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_description = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_language = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_modules = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_tasks = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_rules = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_style_guide = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_test_framework = Mock(return_value={'project_name': 'test'})
        self.claude_setup._finalize_project_data = Mock(return_value={'project_name': 'test'})
        
        result = self.claude_setup.run(self.test_project_name)
        
        assert self.claude_setup._collect_project_type.call_args[0][1] is True
    
    def test_run_with_claude_preset(self):
        """Test run with Claude enhancement preset."""
        # Mock all collection methods
        self.claude_setup._collect_project_type = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_description = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_language = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_modules = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_tasks = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_rules = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_style_guide = Mock(return_value={'project_name': 'test'})
        self.claude_setup._collect_test_framework = Mock(return_value={'project_name': 'test'})
        self.claude_setup._finalize_project_data = Mock(return_value={'project_name': 'test'})
        
        result = self.claude_setup.run(self.test_project_name, use_claude=True)
        
        assert self.claude_setup._collect_project_type.call_args[0][1] is True
    
    @patch('questionary.select')
    def test_collect_project_type_without_claude(self, mock_select):
        """Test collecting project type without Claude."""
        mock_select.return_value.ask.return_value = 'web'
        project_data = {'metadata': {}}
        
        result = self.claude_setup._collect_project_type(project_data, use_claude=False)
        
        assert result['metadata']['project_type'] == 'web'
        assert result['metadata']['project_type_name'] == 'Web Application'
    
    @patch('questionary.select')
    def test_collect_project_type_with_claude(self, mock_select):
        """Test collecting project type with Claude enhancement."""
        mock_select.return_value.ask.return_value = 'web'
        project_data = {'project_name': 'test', 'metadata': {}}
        
        # Mock Claude response
        claude_response = {
            'project_type_analysis': 'Based on the name, this appears to be a web project',
            'recommended_type': 'web',
            'confidence': 0.9
        }
        self.claude_setup.processor._run_claude = Mock(return_value=json.dumps(claude_response))
        
        with patch('questionary.confirm') as mock_confirm:
            mock_confirm.return_value.ask.return_value = True
            result = self.claude_setup._collect_project_type(project_data, use_claude=True)
        
        assert result['metadata']['project_type'] == 'web'
    
    @patch('questionary.text')
    def test_collect_description_without_claude(self, mock_text):
        """Test collecting description without Claude."""
        mock_text.return_value.ask.return_value = 'A test project'
        project_data = {'metadata': {}}
        
        result = self.claude_setup._collect_description(project_data, use_claude=False)
        
        assert result['metadata']['description'] == 'A test project'
    
    @patch('questionary.text')
    @patch('questionary.confirm')
    def test_collect_description_with_claude(self, mock_confirm, mock_text):
        """Test collecting description with Claude enhancement."""
        mock_text.return_value.ask.return_value = 'A test project'
        mock_confirm.return_value.ask.return_value = True
        project_data = {
            'project_name': 'test',
            'metadata': {'project_type': 'web'}
        }
        
        # Mock Claude response
        claude_response = {
            'enhanced_description': 'A comprehensive test project for web development',
            'key_features': ['Feature 1', 'Feature 2']
        }
        self.claude_setup.processor._run_claude = Mock(return_value=json.dumps(claude_response))
        
        result = self.claude_setup._collect_description(project_data, use_claude=True)
        
        assert 'description' in result['metadata']
    
    @patch('questionary.checkbox')
    @patch('questionary.confirm')
    def test_collect_modules_without_claude(self, mock_confirm, mock_checkbox):
        """Test collecting modules without Claude."""
        mock_checkbox.return_value.ask.return_value = ['authentication', 'database']
        mock_confirm.return_value.ask.side_effect = [False]  # Don't add custom modules
        
        project_data = {
            'metadata': {
                'project_type': 'web',
                'project_type_name': 'Web Application'
            }
        }
        
        result = self.claude_setup._collect_modules(project_data, use_claude=False)
        
        assert 'modules' in result
        assert len(result['modules']) == 2
    
    @patch('questionary.checkbox')
    @patch('questionary.confirm')
    def test_collect_modules_with_claude(self, mock_confirm, mock_checkbox):
        """Test collecting modules with Claude enhancement."""
        mock_checkbox.return_value.ask.return_value = ['authentication']
        mock_confirm.return_value.ask.side_effect = [True, False]  # Use Claude suggestions, don't add more
        
        project_data = {
            'project_name': 'test',
            'metadata': {
                'project_type': 'web',
                'description': 'A web app'
            }
        }
        
        # Mock Claude response
        claude_response = {
            'suggested_modules': [
                {'name': 'auth', 'description': 'Enhanced auth module'},
                {'name': 'api', 'description': 'API endpoints'}
            ]
        }
        self.claude_setup.processor._run_claude = Mock(return_value=json.dumps(claude_response))
        
        result = self.claude_setup._collect_modules(project_data, use_claude=True)
        
        assert 'modules' in result
    
    def test_add_conversation_history(self):
        """Test adding to conversation history."""
        self.claude_setup._add_to_conversation('user', 'test message')
        
        assert len(self.claude_setup.conversation_history) == 1
        assert self.claude_setup.conversation_history[0]['role'] == 'user'
        assert self.claude_setup.conversation_history[0]['content'] == 'test message'
    
    def test_get_claude_suggestion_success(self):
        """Test getting Claude suggestion successfully."""
        prompt = "Test prompt"
        expected_response = {'suggestion': 'Test suggestion'}
        
        self.claude_setup.processor._run_claude = Mock(return_value=json.dumps(expected_response))
        
        result = self.claude_setup._get_claude_suggestion(prompt, expected_response)
        
        assert result == expected_response
    
    def test_get_claude_suggestion_invalid_json(self):
        """Test getting Claude suggestion with invalid JSON."""
        prompt = "Test prompt"
        default = {'default': 'value'}
        
        self.claude_setup.processor._run_claude = Mock(return_value='Invalid JSON')
        
        result = self.claude_setup._get_claude_suggestion(prompt, default)
        
        assert result == default
    
    def test_get_claude_suggestion_no_response(self):
        """Test getting Claude suggestion with no response."""
        prompt = "Test prompt"
        default = {'default': 'value'}
        
        self.claude_setup.processor._run_claude = Mock(return_value=None)
        
        result = self.claude_setup._get_claude_suggestion(prompt, default)
        
        assert result == default
    
    @patch('questionary.select')
    def test_collect_language(self, mock_select):
        """Test collecting language preference."""
        mock_select.return_value.ask.return_value = 'Python'
        project_data = {'metadata': {}}
        
        result = self.claude_setup._collect_language(project_data, use_claude=False)
        
        assert result['metadata']['language'] == 'Python'
    
    @patch('questionary.confirm')
    def test_collect_tasks_empty_modules(self, mock_confirm):
        """Test collecting tasks with empty modules."""
        project_data = {'modules': []}
        
        result = self.claude_setup._collect_tasks(project_data, use_claude=False)
        
        assert 'tasks' in result
        assert result['tasks'] == []
    
    def test_finalize_project_data(self):
        """Test finalizing project data."""
        project_data = {
            'project_name': 'test',
            'modules': [{'name': 'core'}],
            'tasks': [{'title': 'Task 1'}],
            'enhanced_with_claude': True
        }
        
        result = self.claude_setup._finalize_project_data(project_data)
        
        assert result == project_data  # Should return unchanged in basic case