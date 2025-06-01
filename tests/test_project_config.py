"""Tests for project configuration."""

import pytest
from src.project_config import ProjectConfig


class TestProjectConfig:
    """Test cases for project configuration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = ProjectConfig()
    
    def test_project_types_exist(self):
        """Test that all project types are defined."""
        expected_types = ['web', 'cli', 'library', 'api', 'ml', 'custom']
        
        for project_type in expected_types:
            assert project_type in self.config.project_types
            assert 'name' in self.config.project_types[project_type]
            assert 'description' in self.config.project_types[project_type]
            assert 'suggested_modules' in self.config.project_types[project_type]
            assert 'suggested_rules' in self.config.project_types[project_type]
    
    def test_style_guides_exist(self):
        """Test that style guides are defined."""
        expected_guides = ['pep8', 'black', 'google', 'custom']
        
        for guide in expected_guides:
            assert guide in self.config.style_guides
    
    def test_test_frameworks_exist(self):
        """Test that test frameworks are defined."""
        expected_frameworks = ['pytest', 'unittest', 'jest', 'mocha', 'custom']
        
        for framework in expected_frameworks:
            assert framework in self.config.test_frameworks
    
    def test_get_suggested_tasks_web(self):
        """Test getting suggested tasks for web projects."""
        tasks = self.config.get_suggested_tasks('web')
        
        assert isinstance(tasks, list)
        assert len(tasks) > 0
        assert 'Set up development environment' in tasks
        assert 'Design database schema' in tasks
    
    def test_get_suggested_tasks_cli(self):
        """Test getting suggested tasks for CLI projects."""
        tasks = self.config.get_suggested_tasks('cli')
        
        assert isinstance(tasks, list)
        assert len(tasks) > 0
        assert 'Define command structure' in tasks
        assert 'Implement argument parsing' in tasks
    
    def test_get_suggested_tasks_custom(self):
        """Test getting suggested tasks for custom projects."""
        tasks = self.config.get_suggested_tasks('custom')
        
        assert isinstance(tasks, list)
        assert len(tasks) == 0
    
    def test_get_suggested_tasks_unknown(self):
        """Test getting suggested tasks for unknown project type."""
        tasks = self.config.get_suggested_tasks('unknown_type')
        
        assert isinstance(tasks, list)
        assert len(tasks) == 0