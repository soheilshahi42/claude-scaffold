"""Tests for Claude enhancer functionality."""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock, call
from src.claude.claude_enhancer import ClaudeEnhancedSetup


class TestClaudeEnhancedSetup:
    """Test cases for Claude enhanced setup."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_interactive_setup = Mock()
        self.enhancer = ClaudeEnhancedSetup(self.mock_interactive_setup)
        self.test_project_data = {
            'project_name': 'test_project',
            'metadata': {
                'project_type': 'web',
                'description': 'Test project'
            },
            'modules': [{'name': 'core', 'description': 'Core module'}],
            'tasks': [{'title': 'Task 1', 'module': 'core'}],
            'rules': ['Rule 1']
        }
    
    @patch('questionary.confirm')
    def test_enhance_with_claude_declined(self, mock_confirm):
        """Test enhancement when user declines Claude assistance."""
        mock_confirm.return_value.ask.return_value = False
        
        result = self.enhancer.enhance_with_claude(self.test_project_data)
        
        assert result == self.test_project_data
        mock_confirm.assert_called_once()
    
    @patch('questionary.confirm')
    def test_enhance_with_claude_accepted(self, mock_confirm):
        """Test enhancement when user accepts Claude assistance."""
        mock_confirm.return_value.ask.return_value = True
        self.enhancer.enhance_project_data = Mock(return_value={'enhanced': True})
        
        result = self.enhancer.enhance_with_claude(self.test_project_data)
        
        assert result == {'enhanced': True}
        self.enhancer.enhance_project_data.assert_called_once_with(self.test_project_data)
    
    @patch('questionary.confirm')
    def test_enhance_project_data_success(self, mock_confirm):
        """Test successful project data enhancement."""
        # Mock processor responses
        enhanced_response = {
            'project_name': 'test_project',
            'enhanced_description': 'Enhanced description',
            'tasks': [
                {'title': 'Task 1', 'module': 'core', 'priority': 'high'}
            ],
            'modules': [
                {'name': 'core', 'description': 'Enhanced core module'}
            ]
        }
        
        self.enhancer.processor.process_project_setup = Mock(return_value=enhanced_response)
        self.enhancer.processor.generate_task_details = Mock(return_value={
            'implementation': 'Task implementation details'
        })
        mock_confirm.return_value.ask.return_value = True  # Review changes
        
        result = self.enhancer.enhance_project_data(self.test_project_data)
        
        assert 'enhanced_description' in result
        assert result['tasks'][0]['details']['implementation'] == 'Task implementation details'
    
    @patch('questionary.confirm')
    def test_enhance_project_data_with_task_details(self, mock_confirm):
        """Test enhancement with task details generation."""
        enhanced_data = {
            'tasks': [
                {'title': 'Task 1', 'module': 'core'},
                {'title': 'Task 2', 'module': 'api', 'details': {'existing': 'details'}}
            ]
        }
        
        self.enhancer.processor.process_project_setup = Mock(return_value=enhanced_data)
        self.enhancer.processor.generate_task_details = Mock(return_value={'new': 'details'})
        mock_confirm.return_value.ask.return_value = True
        
        result = self.enhancer.enhance_project_data(self.test_project_data)
        
        # Should only generate details for task without existing details
        assert self.enhancer.processor.generate_task_details.call_count == 1
        assert result['tasks'][0]['details'] == {'new': 'details'}
        assert result['tasks'][1]['details'] == {'existing': 'details'}
    
    def test_enhance_project_data_processor_failure(self):
        """Test enhancement when processor fails."""
        self.enhancer.processor.process_project_setup = Mock(return_value=None)
        
        result = self.enhancer.enhance_project_data(self.test_project_data)
        
        assert result == self.test_project_data
    
    @patch('questionary.confirm')
    def test_enhance_project_data_exception_handling(self, mock_confirm):
        """Test enhancement with exception handling."""
        self.enhancer.processor.process_project_setup = Mock(side_effect=Exception("Test error"))
        
        result = self.enhancer.enhance_project_data(self.test_project_data)
        
        assert result == self.test_project_data
    
    def test_review_changes_accepted(self):
        """Test reviewing changes when accepted."""
        original = {'key': 'original'}
        enhanced = {'key': 'enhanced', 'new_key': 'new_value'}
        
        with patch('questionary.confirm') as mock_confirm:
            mock_confirm.return_value.ask.return_value = True
            
            result = self.enhancer._review_changes(original, enhanced)
            
            assert result == enhanced
    
    def test_review_changes_declined(self):
        """Test reviewing changes when declined."""
        original = {'key': 'original'}
        enhanced = {'key': 'enhanced'}
        
        with patch('questionary.confirm') as mock_confirm:
            mock_confirm.return_value.ask.return_value = False
            
            result = self.enhancer._review_changes(original, enhanced)
            
            assert result == original
    
    def test_display_enhancements(self, capsys):
        """Test displaying enhancements."""
        enhancements = {
            'enhanced_description': 'New enhanced description',
            'additional_rules': ['Rule 1', 'Rule 2'],
            'architecture': {'pattern': 'MVC'},
            'module_enhancements': {
                'core': {'enhanced': 'Enhanced core description'}
            }
        }
        
        self.enhancer._display_enhancements(enhancements)
        
        captured = capsys.readouterr()
        assert 'Enhanced Description:' in captured.out
        assert 'New enhanced description' in captured.out
        assert 'Additional Rules:' in captured.out
        assert 'Rule 1' in captured.out
        assert 'Architecture Recommendations:' in captured.out
        assert 'Module Enhancements:' in captured.out
    
    def test_merge_enhancements(self):
        """Test merging enhancements into project data."""
        project_data = {
            'description': 'Original description',
            'modules': [{'name': 'core', 'description': 'Original core'}],
            'rules': ['Original rule']
        }
        
        enhancements = {
            'enhanced_description': 'Enhanced description',
            'module_enhancements': {
                'core': {'enhanced_description': 'Enhanced core description'}
            },
            'additional_rules': ['New rule 1', 'New rule 2']
        }
        
        result = self.enhancer._merge_enhancements(project_data, enhancements)
        
        assert result['description'] == 'Enhanced description'
        assert result['modules'][0]['description'] == 'Enhanced core description'
        assert len(result['rules']) == 3
        assert 'New rule 1' in result['rules']
    
    def test_merge_enhancements_missing_module(self):
        """Test merging enhancements when module doesn't exist."""
        project_data = {
            'modules': [{'name': 'core', 'description': 'Core'}]
        }
        
        enhancements = {
            'module_enhancements': {
                'api': {'enhanced_description': 'API description'}
            }
        }
        
        result = self.enhancer._merge_enhancements(project_data, enhancements)
        
        # Should not crash, module not found is ignored
        assert result['modules'][0]['description'] == 'Core'