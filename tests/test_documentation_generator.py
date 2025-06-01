"""Tests for documentation generation."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.documentation_generator import DocumentationGenerator


class TestDocumentationGenerator:
    """Test cases for documentation generation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.doc_gen = DocumentationGenerator()
    
    @patch('src.documentation_generator.Path.write_text')
    def test_create_todo_file(self, mock_write):
        """Test creating a TODO file."""
        todo_items = [
            '- [ ] Task 1',
            '- [ ] Task 2',
            '- [x] Task 3'
        ]
        
        self.doc_gen.create_todo_file(
            Path('/test/TODO.md'),
            'test_module',
            'the test module',
            todo_items
        )
        
        mock_write.assert_called_once()
        content = mock_write.call_args[0][0]
        
        assert 'test_module' in content
        assert 'the test module' in content
        assert '- [ ] Task 1' in content
        assert '1/3 tasks completed (33%)' in content
    
    @patch('src.documentation_generator.Path.write_text')
    @patch('src.documentation_generator.Path.mkdir')
    def test_generate_documentation_basic(self, mock_mkdir, mock_write):
        """Test basic documentation generation."""
        project_data = {
            'project_name': 'test_project',
            'modules': [
                {'name': 'core', 'description': 'Core functionality'}
            ],
            'tasks': [],
            'metadata': {
                'description': 'Test project',
                'project_type': 'custom',
                'language': 'Python'
            }
        }
        
        self.doc_gen.generate_documentation(Path('/test'), project_data)
        
        # Verify files were created
        assert mock_write.call_count >= 4  # root_claude, global_rules, tasks_md, TODO.md
    
    @patch('src.documentation_generator.Path.write_text')
    @patch('src.documentation_generator.Path.mkdir')
    def test_generate_documentation_with_claude_enhancements(self, mock_mkdir, mock_write):
        """Test documentation generation with Claude enhancements."""
        project_data = {
            'project_name': 'test_project',
            'modules': [{
                'name': 'api',
                'description': 'API module',
                'documentation': {
                    'responsibilities': 'Handle API requests',
                    'public_api': 'GET /users, POST /users',
                    'architecture': 'RESTful design',
                    'dependencies': [{'name': 'FastAPI', 'purpose': 'Web framework'}]
                }
            }],
            'tasks': [{
                'title': 'Create user endpoint',
                'module': 'api',
                'priority': 'high',
                'details': {
                    'goal': 'Implement user creation',
                    'subtasks': ['Design schema', 'Write tests', 'Implement endpoint']
                }
            }],
            'metadata': {
                'description': 'Test API project',
                'project_type': 'api',
                'language': 'Python'
            }
        }
        
        self.doc_gen.generate_documentation(Path('/test'), project_data)
        
        # Verify enhanced content was used
        written_contents = [call[0][0] for call in mock_write.call_args_list]
        
        # Check that enhanced content appears in module documentation
        module_content = next((c for c in written_contents if 'Handle API requests' in c), None)
        assert module_content is not None
        assert 'RESTful design' in module_content