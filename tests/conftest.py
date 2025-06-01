"""Shared pytest fixtures and configuration for Claude Scaffold tests."""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test operations."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_project_data():
    """Standard project data for testing."""
    return {
        'project_name': 'test_project',
        'timestamp': '2024-01-01T00:00:00',
        'version': '0.1.0',
        'enhanced_with_claude': True,
        'modules': [
            {'name': 'frontend', 'description': 'React frontend module'},
            {'name': 'backend', 'description': 'Django backend module'},
            {'name': 'api', 'description': 'REST API module'}
        ],
        'tasks': [
            {
                'title': 'Set up Django REST framework',
                'module': 'backend',
                'priority': 'high'
            },
            {
                'title': 'Create React components',
                'module': 'frontend',
                'priority': 'medium'
            },
            {
                'title': 'Design API endpoints',
                'module': 'api',
                'priority': 'high'
            }
        ],
        'rules': {
            'suggested': [
                'Follow PEP 8 for Python code',
                'Use TypeScript for React components',
                'Write tests before implementation'
            ],
            'custom': ['Document all API endpoints']
        },
        'constraints': ['Python 3.8+', 'Node.js 16+', 'PostgreSQL 12+'],
        'metadata': {
            'project_type': 'web',
            'project_type_name': 'Web Application',
            'description': 'A full-stack todo application with React and Django',
            'language': 'Both',
            'style_guide': 'pep8',
            'test_framework': 'pytest',
            'commands': {
                'install': 'pip install -r requirements.txt && npm install',
                'test': 'pytest && npm test',
                'build': 'python manage.py collectstatic && npm run build',
                'dev': 'python manage.py runserver & npm start',
                'lint': 'flake8 && eslint src/'
            },
            'git': {
                'init': True,
                'initial_branch': 'main'
            }
        }
    }


@pytest.fixture
def mock_claude_processor():
    """Mock ClaudeProcessor for testing."""
    processor = Mock()
    processor._call_claude = MagicMock(return_value='{"status": "success"}')
    processor.check_claude_available = MagicMock(return_value=True)
    processor.claude_executable = 'claude'
    return processor


@pytest.fixture
def mock_questionary():
    """Mock questionary for interactive testing."""
    with patch('questionary.text') as mock_text, \
         patch('questionary.select') as mock_select, \
         patch('questionary.confirm') as mock_confirm, \
         patch('questionary.checkbox') as mock_checkbox:
        
        # Set up default returns
        mock_text.return_value.ask.return_value = 'test_input'
        mock_select.return_value.ask.return_value = 'test_selection'
        mock_confirm.return_value.ask.return_value = True
        mock_checkbox.return_value.ask.return_value = ['option1', 'option2']
        
        yield {
            'text': mock_text,
            'select': mock_select,
            'confirm': mock_confirm,
            'checkbox': mock_checkbox
        }


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for command execution."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = 'Success'
        mock_run.return_value.stderr = ''
        yield mock_run


@pytest.fixture
def sample_template_context():
    """Sample context for template rendering."""
    return {
        'project_name': 'test_project',
        'project_description': 'A test project',
        'timestamp': datetime.now().isoformat(),
        'modules': [
            {'name': 'core', 'description': 'Core functionality'}
        ],
        'tasks_by_module': {
            'core': [
                {'title': 'Implement core feature', 'priority': 'high'}
            ]
        },
        'rules_list': ['Follow TDD', 'Write documentation'],
        'constraints_list': ['Python 3.8+'],
        'project_structure': '- src/\n  - core/\n    - __init__.py',
        'module_overview': '- **core**: Core functionality',
        'commands': {
            'test': 'pytest',
            'build': 'python setup.py build'
        }
    }


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests."""
    # Add any singleton resets here if needed
    yield