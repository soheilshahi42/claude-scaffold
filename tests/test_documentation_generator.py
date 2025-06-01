"""Tests for documentation generator functionality."""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock, call
from src.core.documentation_generator import DocumentationGenerator


class TestDocumentationGenerator:
    """Test cases for documentation generation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.doc_generator = DocumentationGenerator()
        self.test_project_path = Path("/tmp/test_project")
        self.test_project_data = {
            'project_name': 'TestProject',
            'description': 'A test project',
            'modules': [
                {'name': 'core', 'description': 'Core module'},
                {'name': 'api', 'description': 'API module'}
            ],
            'tasks': [
                {'module': 'core', 'title': 'Task 1', 'priority': 'high'},
                {'module': 'api', 'title': 'Task 2', 'priority': 'medium'}
            ],
            'rules': ['Rule 1', 'Rule 2'],
            'style_guide': 'pep8',
            'test_framework': 'pytest'
        }
    
    @patch('pathlib.Path.write_text')
    def test_generate_documentation_basic(self, mock_write):
        """Test basic documentation generation."""
        self.doc_generator.helpers.prepare_template_context = Mock(return_value={})
        self.doc_generator.templates.get_template = Mock(return_value="Template content")
        self.doc_generator.formatters.organize_tasks_by_module = Mock(return_value={})
        self.doc_generator.create_todo_file = Mock()
        self.doc_generator.create_module_readme = Mock()
        
        self.doc_generator.generate_documentation(self.test_project_path, self.test_project_data)
        
        # Verify all main documentation files are created
        expected_files = ['CLAUDE.md', 'GLOBAL_RULES.md', 'TASKS.md']
        assert self.doc_generator.templates.get_template.call_count >= len(expected_files)
        assert mock_write.call_count >= len(expected_files)
    
    @patch('pathlib.Path.write_text')
    def test_generate_documentation_with_modules(self, mock_write):
        """Test documentation generation with modules."""
        self.doc_generator.helpers.prepare_template_context = Mock(return_value={})
        self.doc_generator.templates.get_template = Mock(return_value="Template content")
        self.doc_generator.formatters.organize_tasks_by_module = Mock(return_value={
            'core': [{'title': 'Task 1', 'priority': 'high'}],
            'api': [{'title': 'Task 2', 'priority': 'medium'}]
        })
        self.doc_generator.create_todo_file = Mock()
        self.doc_generator.create_module_readme = Mock()
        
        self.doc_generator.generate_documentation(self.test_project_path, self.test_project_data)
        
        # Verify module documentation is created
        assert self.doc_generator.create_module_readme.call_count == 2
    
    @patch('pathlib.Path.mkdir')
    @patch('pathlib.Path.write_text')
    def test_create_module_readme(self, mock_write, mock_mkdir):
        """Test creating module README files."""
        module_data = {
            'name': 'core',
            'description': 'Core functionality',
            'tasks': [
                {'title': 'Implement feature', 'priority': 'high'},
                {'title': 'Write tests', 'priority': 'medium'}
            ]
        }
        
        self.doc_generator.create_module_readme(self.test_project_path, module_data)
        
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_write.assert_called_once()
        
        # Check README content
        readme_content = mock_write.call_args[0][0]
        assert '# Core Module' in readme_content
        assert 'Core functionality' in readme_content
        assert '## Tasks' in readme_content
        assert '- [ ] [HIGH] Implement feature' in readme_content
        assert '- [ ] [MEDIUM] Write tests' in readme_content
    
    @patch('pathlib.Path.write_text')
    def test_create_todo_file(self, mock_write):
        """Test creating TODO files."""
        todos = [
            "Complete task 1",
            "Complete task 2"
        ]
        
        self.doc_generator.create_todo_file(
            self.test_project_path / 'TODO.md',
            'TestProject',
            'core module',
            todos
        )
        
        mock_write.assert_called_once()
        todo_content = mock_write.call_args[0][0]
        assert '# TODO - TestProject' in todo_content
        assert 'TODO list for core module' in todo_content
        assert '- [ ] Complete task 1' in todo_content
        assert '- [ ] Complete task 2' in todo_content
    
    def test_generate_module_todos(self):
        """Test generating module-specific TODOs."""
        tasks = [
            {'title': 'Task 1', 'priority': 'high'},
            {'title': 'Task 2', 'priority': 'low'}
        ]
        
        todos = self.doc_generator.generate_module_todos(tasks)
        
        assert len(todos) == 2
        assert todos[0] == '[HIGH] Task 1'
        assert todos[1] == '[LOW] Task 2'
    
    def test_generate_module_todos_empty(self):
        """Test generating TODOs with empty task list."""
        todos = self.doc_generator.generate_module_todos([])
        
        assert len(todos) == 1
        assert todos[0] == 'Add initial tasks for this module'
    
    @patch('pathlib.Path.write_text')
    def test_create_testing_docs(self, mock_write):
        """Test creating testing documentation."""
        self.doc_generator.templates.get_template = Mock(return_value="Testing template")
        
        self.doc_generator.create_testing_docs(self.test_project_path, self.test_project_data)
        
        mock_write.assert_called()
        self.doc_generator.templates.get_template.assert_called_with('testing_md', {
            'project_name': 'TestProject',
            'test_framework': 'pytest'
        })
    
    @patch('pathlib.Path.write_text')
    def test_generate_documentation_no_modules(self, mock_write):
        """Test documentation generation with no modules."""
        project_data = {
            'project_name': 'TestProject',
            'description': 'A test project',
            'modules': [],
            'tasks': []
        }
        
        self.doc_generator.helpers.prepare_template_context = Mock(return_value={})
        self.doc_generator.templates.get_template = Mock(return_value="Template content")
        self.doc_generator.formatters.organize_tasks_by_module = Mock(return_value={})
        self.doc_generator.create_todo_file = Mock()
        
        self.doc_generator.generate_documentation(self.test_project_path, project_data)
        
        # Should still create main documentation files
        assert self.doc_generator.templates.get_template.call_count >= 3
    
    def test_generate_module_todos_mixed_priorities(self):
        """Test generating TODOs with mixed priority levels."""
        tasks = [
            {'title': 'Critical task', 'priority': 'critical'},
            {'title': 'High task', 'priority': 'high'},
            {'title': 'Medium task', 'priority': 'medium'},
            {'title': 'Low task', 'priority': 'low'}
        ]
        
        todos = self.doc_generator.generate_module_todos(tasks)
        
        assert len(todos) == 4
        assert '[CRITICAL]' in todos[0]
        assert '[HIGH]' in todos[1]
        assert '[MEDIUM]' in todos[2]
        assert '[LOW]' in todos[3]
    
    @patch('pathlib.Path.mkdir')
    @patch('pathlib.Path.write_text')
    def test_create_module_readme_no_tasks(self, mock_write, mock_mkdir):
        """Test creating module README with no tasks."""
        module_data = {
            'name': 'utils',
            'description': 'Utility functions',
            'tasks': []
        }
        
        self.doc_generator.create_module_readme(self.test_project_path, module_data)
        
        mock_write.assert_called_once()
        readme_content = mock_write.call_args[0][0]
        assert '# Utils Module' in readme_content
        assert 'No tasks defined yet' in readme_content