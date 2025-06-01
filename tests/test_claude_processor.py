"""Comprehensive tests for ClaudeProcessor."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import subprocess
import json

from src.claude.claude_processor import ClaudeProcessor


class TestClaudeProcessor:
    """Test cases for ClaudeProcessor."""
    
    @pytest.fixture
    def processor(self):
        """Create ClaudeProcessor instance."""
        with patch('shutil.which') as mock_which:
            mock_which.return_value = '/usr/bin/claude'
            return ClaudeProcessor()
    
    def test_initialization_claude_found(self):
        """Test initialization when Claude is found."""
        with patch('shutil.which') as mock_which:
            mock_which.return_value = '/usr/bin/claude'
            processor = ClaudeProcessor()
            
            assert processor.claude_executable == '/usr/bin/claude'
            mock_which.assert_called_once_with('claude')
    
    def test_initialization_claude_not_found(self):
        """Test initialization when Claude is not found."""
        with patch('shutil.which') as mock_which:
            mock_which.return_value = None
            processor = ClaudeProcessor()
            
            assert processor.claude_executable == 'claude'
    
    @patch('subprocess.run')
    def test_check_claude_available_success(self, mock_run, processor):
        """Test Claude availability check - success."""
        mock_run.return_value.returncode = 0
        
        result = processor.check_claude_available()
        
        assert result is True
        mock_run.assert_called_once_with(
            [processor.claude_executable, '--version'],
            capture_output=True,
            text=True
        )
    
    @patch('subprocess.run')
    def test_check_claude_available_failure(self, mock_run, processor):
        """Test Claude availability check - failure."""
        mock_run.return_value.returncode = 1
        
        result = processor.check_claude_available()
        
        assert result is False
    
    @patch('subprocess.run')
    def test_check_claude_available_not_found(self, mock_run, processor):
        """Test Claude availability check - command not found."""
        mock_run.side_effect = FileNotFoundError()
        
        result = processor.check_claude_available()
        
        assert result is False
    
    @patch('subprocess.run')
    def test_call_claude_success(self, mock_run, processor):
        """Test successful Claude call."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Claude response"
        mock_run.return_value.stderr = ""
        
        result = processor._call_claude("Test prompt")
        
        assert result == "Claude response"
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == processor.claude_executable
        assert call_args[1] == '-p'
        # The prompt now includes the system prompt prepended
        assert "helpful assistant" in call_args[2]
        assert "Test prompt" in call_args[2]
    
    @patch('subprocess.run')
    def test_call_claude_with_timeout(self, mock_run, processor):
        """Test Claude call with custom timeout."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Response"
        
        result = processor._call_claude("Prompt", timeout=120)
        
        assert result == "Response"
        assert mock_run.call_args[1]['timeout'] == 120
    
    @patch('subprocess.run')
    def test_call_claude_timeout_error(self, mock_run, processor):
        """Test Claude call timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=['claude'], timeout=60
        )
        
        with pytest.raises(TimeoutError) as exc_info:
            processor._call_claude("Test prompt")
        
        assert "timed out after 60 seconds" in str(exc_info.value)
    
    @patch('subprocess.run')
    def test_call_claude_subprocess_error(self, mock_run, processor):
        """Test Claude call subprocess error."""
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=['claude'],
            stderr="Error message"
        )
        
        with pytest.raises(RuntimeError) as exc_info:
            processor._call_claude("Test prompt")
        
        assert "failed with return code 1" in str(exc_info.value)
        assert "Error message" in str(exc_info.value)
    
    @patch('subprocess.run')
    def test_call_claude_file_not_found(self, mock_run, processor):
        """Test Claude executable not found."""
        mock_run.side_effect = FileNotFoundError()
        
        with pytest.raises(RuntimeError) as exc_info:
            processor._call_claude("Test prompt")
        
        assert "not found" in str(exc_info.value)
    
    @patch('subprocess.run')
    def test_call_claude_generic_exception(self, mock_run, processor):
        """Test generic exception handling."""
        mock_run.side_effect = Exception("Unexpected error")
        
        with pytest.raises(RuntimeError) as exc_info:
            processor._call_claude("Test prompt")
        
        assert "Unexpected error calling Claude" in str(exc_info.value)
    
    def test_process_for_module_research_success(self, processor):
        """Test successful module research processing."""
        processor._call_claude = Mock(return_value=json.dumps({
            "responsibilities": ["Handle API requests", "Validate data"],
            "public_api": "get_user(), create_user()",
            "dependencies": ["database", "auth"],
            "examples": ["from api import get_user"],
            "architecture": "RESTful design pattern",
            "error_handling": "Use custom exceptions",
            "performance": "Cache frequently accessed data",
            "security": "Validate all inputs"
        }))
        
        result = processor.process_for_module_research("api", {"project_name": "test"})
        
        assert result is not None
        assert "responsibilities" in result
        assert len(result["responsibilities"]) == 2
        assert "public_api" in result
        assert "dependencies" in result
    
    def test_process_for_module_research_invalid_json(self, processor):
        """Test module research with invalid JSON response."""
        processor._call_claude = Mock(return_value="Not valid JSON")
        
        result = processor.process_for_module_research("api", {"project_name": "test"})
        
        assert result is None
    
    def test_process_for_module_research_exception(self, processor):
        """Test module research with exception."""
        processor._call_claude = Mock(side_effect=Exception("Error"))
        
        result = processor.process_for_module_research("api", {"project_name": "test"})
        
        assert result is None
    
    def test_process_for_task_details_success(self, processor):
        """Test successful task details processing."""
        processor._call_claude = Mock(return_value=json.dumps({
            "goal": "Implement secure user authentication",
            "subtasks": [
                "Design authentication schema",
                "Implement login endpoint",
                "Add password hashing"
            ],
            "research_topics": [
                "OAuth 2.0 best practices",
                "JWT token management"
            ]
        }))
        
        result = processor.process_for_task_details(
            {"title": "Build auth", "module": "auth"},
            {"project_name": "test"}
        )
        
        assert result is not None
        assert result["goal"] == "Implement secure user authentication"
        assert len(result["subtasks"]) == 3
        assert len(result["research_topics"]) == 2
    
    def test_process_for_task_details_invalid_response(self, processor):
        """Test task details with invalid response."""
        processor._call_claude = Mock(return_value="Invalid")
        
        result = processor.process_for_task_details(
            {"title": "Task", "module": "mod"},
            {"project_name": "test"}
        )
        
        assert result is None
    
    def test_process_for_project_enhancement_success(self, processor):
        """Test successful project enhancement."""
        project_data = {
            "project_name": "test",
            "modules": [{"name": "api", "description": "API module"}],
            "tasks": [{"title": "Build API", "module": "api"}]
        }
        
        # Mock responses for each call
        processor._call_claude = Mock()
        processor._call_claude.side_effect = [
            # Module research response
            json.dumps({
                "responsibilities": ["Handle requests"],
                "public_api": "get_data()",
                "dependencies": []
            }),
            # Task details response
            json.dumps({
                "goal": "Build REST API",
                "subtasks": ["Design endpoints"],
                "research_topics": ["REST principles"]
            })
        ]
        
        result = processor.process_for_project_enhancement(project_data)
        
        assert result is not None
        assert result["enhanced_with_claude"] is True
        assert "documentation" in result["modules"][0]
        assert "details" in result["tasks"][0]
    
    def test_process_for_project_enhancement_partial_success(self, processor):
        """Test project enhancement with partial failures."""
        project_data = {
            "project_name": "test",
            "modules": [{"name": "api", "description": "API"}],
            "tasks": [{"title": "Task", "module": "api"}]
        }
        
        # First call succeeds, second fails
        processor._call_claude = Mock()
        processor._call_claude.side_effect = [
            json.dumps({"responsibilities": ["Test"]}),
            "Invalid JSON"
        ]
        
        result = processor.process_for_project_enhancement(project_data)
        
        assert result is not None
        assert result["enhanced_with_claude"] is True
        assert "documentation" in result["modules"][0]
        assert "details" not in result["tasks"][0]  # Failed to enhance
    
    def test_process_for_project_enhancement_all_failures(self, processor):
        """Test project enhancement when all calls fail."""
        project_data = {
            "project_name": "test",
            "modules": [{"name": "api", "description": "API"}],
            "tasks": []
        }
        
        processor._call_claude = Mock(side_effect=Exception("Error"))
        
        result = processor.process_for_project_enhancement(project_data)
        
        assert result is not None
        assert result["enhanced_with_claude"] is True
        assert result["modules"] == project_data["modules"]  # Unchanged
    
    def test_prompt_generation_module_research(self, processor):
        """Test prompt generation for module research."""
        # Access the private method through name mangling
        prompt = processor._call_claude("test prompt")
        
        # Just verify the method can be called with proper args
        processor._call_claude = Mock(return_value="{}")
        processor.process_for_module_research("api", {"project_name": "test"})
        
        # Check that prompt contains expected elements
        call_args = processor._call_claude.call_args[0][0]
        assert "api module" in call_args
        assert "responsibilities" in call_args
        assert "public_api" in call_args