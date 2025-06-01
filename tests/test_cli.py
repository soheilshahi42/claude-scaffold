import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path


class TestCLI:
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_cli_help(self):
        result = subprocess.run(
            ["python", "-m", "src.cli", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Claude Scaffold" in result.stdout
        assert "new" in result.stdout
        assert "add-task" in result.stdout
    
    def test_cli_new_command_help(self):
        result = subprocess.run(
            ["python", "-m", "src.cli", "new", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "project_name" in result.stdout
        assert "--force" in result.stdout
        assert "--no-interactive" in result.stdout
    
    def test_cli_add_task_help(self):
        result = subprocess.run(
            ["python", "-m", "src.cli", "add-task", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "project_path" in result.stdout
        assert "module" in result.stdout
        assert "task_title" in result.stdout