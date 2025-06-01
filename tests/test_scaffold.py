import pytest
import tempfile
import shutil
from pathlib import Path
from src.scaffold import ClaudeScaffold


class TestClaudeScaffold:
    @pytest.fixture
    def scaffold(self):
        return ClaudeScaffold()
    
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_create_project_basic(self, scaffold, temp_dir):
        project_name = "test_project"
        project_path = temp_dir / project_name
        
        result = scaffold.create_project(
            project_name=project_name,
            project_path=project_path,
            interactive=False
        )
        
        assert result is True
        assert project_path.exists()
        assert (project_path / "CLAUDE.md").exists()
        assert (project_path / "GLOBAL_RULES.md").exists()
        assert (project_path / "TASKS.md").exists()
        assert (project_path / "TODO.md").exists()
        assert (project_path / "tests").exists()
    
    def test_create_project_with_modules(self, scaffold, temp_dir):
        project_name = "test_project"
        project_path = temp_dir / project_name
        
        project_data = {
            'project_name': project_name,
            'timestamp': '2024-01-01T00:00:00',
            'modules': [
                {'name': 'audio', 'description': 'Audio processing module'},
                {'name': 'auth', 'description': 'Authentication module'}
            ],
            'tasks': [
                {'title': 'Implement audio resampling', 'module': 'audio'},
                {'title': 'Build authentication middleware', 'module': 'auth'}
            ],
            'rules': {'custom': ['Follow PEP8', 'Use type hints']},
            'constraints': ['Python 3.8+', 'No external dependencies']
        }
        
        # These methods no longer exist on ClaudeScaffold
        # They are now in ProjectCreator and DocumentationGenerator
        # This test needs to be rewritten or removed
        
        assert (project_path / "audio").exists()
        assert (project_path / "audio" / "CLAUDE.md").exists()
        assert (project_path / "audio" / "TODO.md").exists()
        assert (project_path / "audio" / "docs").exists()
        assert (project_path / "audio" / "__init__.py").exists()
        
        assert (project_path / "auth").exists()
        assert (project_path / "auth" / "CLAUDE.md").exists()
        assert (project_path / "auth" / "TODO.md").exists()
        assert (project_path / "auth" / "docs").exists()
        assert (project_path / "auth" / "__init__.py").exists()
        
        assert (project_path / "tests" / "audio").exists()
        assert (project_path / "tests" / "auth").exists()
    
    def test_create_project_already_exists(self, scaffold, temp_dir):
        project_name = "test_project"
        project_path = temp_dir / project_name
        project_path.mkdir()
        
        result = scaffold.create_project(
            project_name=project_name,
            project_path=project_path,
            force=False,
            interactive=False
        )
        
        assert result is False
    
    def test_create_project_force_overwrite(self, scaffold, temp_dir):
        project_name = "test_project"
        project_path = temp_dir / project_name
        project_path.mkdir()
        (project_path / "existing_file.txt").touch()
        
        result = scaffold.create_project(
            project_name=project_name,
            project_path=project_path,
            force=True,
            interactive=False
        )
        
        assert result is True
        assert not (project_path / "existing_file.txt").exists()
        assert (project_path / "CLAUDE.md").exists()
    
    def test_add_task(self, scaffold, temp_dir):
        project_name = "test_project"
        project_path = temp_dir / project_name
        
        project_data = {
            'project_name': project_name,
            'timestamp': '2024-01-01T00:00:00',
            'modules': [{'name': 'audio', 'description': 'Audio processing module'}],
            'tasks': [],
            'rules': {},
            'constraints': []
        }
        
        # These methods no longer exist on ClaudeScaffold
        # They are now in ProjectCreator and DocumentationGenerator
        # This test needs to be rewritten or removed
        
        result = scaffold.add_task(project_path, 'audio', 'New audio task')
        
        assert result is True
        
        with open(project_path / 'TASKS.md', 'r') as f:
            content = f.read()
            assert 'New audio task' in content
        
        with open(project_path / 'audio' / 'CLAUDE.md', 'r') as f:
            content = f.read()
            assert 'New audio task' in content
    
    def test_scaffold_initialization(self, scaffold):
        # Test that scaffold has the required components
        assert hasattr(scaffold, 'project_creator')
        assert hasattr(scaffold, 'task_manager')
    
    def test_todo_file_creation(self, scaffold, temp_dir):
        todo_path = temp_dir / "TODO.md"
        todo_items = [
            "- [ ] Task 1",
            "- [ ] Task 2",
            "- [ ] Task 3"
        ]
        
        # This method no longer exists on ClaudeScaffold
        # It's now in DocumentationGenerator
        # This test needs to be rewritten or removed
        
        assert todo_path.exists()
        
        with open(todo_path, 'r') as f:
            content = f.read()
            assert "Test Scope TODO List" in content
            assert "Total tasks: 3" in content
            assert "Completed: 0" in content
            assert "Pending: 3" in content
            assert all(item in content for item in todo_items)