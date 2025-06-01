import sys
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional, Any

from .interactive import InteractiveSetup
from .templates import ProjectTemplates
from .documentation_generator import DocumentationGenerator
from .project_helpers import ProjectHelpers


class ProjectCreator:
    """Handles the main project creation workflow."""
    
    def __init__(self):
        self.templates = ProjectTemplates()
        self.interactive_setup = InteractiveSetup()
        self.doc_generator = DocumentationGenerator()
        self.helpers = ProjectHelpers()
    
    def check_claude_available(self) -> bool:
        """Check if Claude CLI is available."""
        try:
            result = subprocess.run(['claude', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Claude CLI detected - intelligent configuration available!")
                return True
        except FileNotFoundError:
            pass
        
        print("⚠️  Claude CLI not found - using standard configuration")
        print("   Install Claude CLI for intelligent project setup: https://github.com/anthropics/claude-code")
        return False
    
    def create_project(self, project_name: str, project_path: Optional[Path] = None, 
                      force: bool = False, interactive: bool = True) -> bool:
        """Create a new Claude Scaffold project."""
        if project_path is None:
            project_path = Path.cwd() / project_name
        
        # Check if project exists
        if project_path.exists() and not force:
            print(f"❌ Error: Project '{project_name}' already exists.", file=sys.stderr)
            print(f"   Use --force to overwrite or choose a different name.", file=sys.stderr)
            return False
        
        if project_path.exists() and force:
            print(f"⚠️  Removing existing project at {project_path}")
            shutil.rmtree(project_path)
        
        try:
            # Run interactive setup if enabled
            if interactive:
                # Check if Claude is available
                use_claude = self.check_claude_available()
                project_data = self.interactive_setup.run(project_name, use_claude=use_claude)
            else:
                # Use minimal defaults for non-interactive mode
                project_data = self.helpers.get_default_project_data(project_name)
            
            # Create project structure
            print(f"\n🚀 Creating project structure...")
            self._create_directory_structure(project_path, project_data)
            
            # Generate all documentation
            print(f"📝 Generating documentation...")
            self.doc_generator.generate_documentation(project_path, project_data)
            
            # Create .claude directory and files
            print(f"🔧 Setting up Claude Code integration...")
            self._create_claude_integration(project_path, project_data)
            
            # Initialize git if requested
            if project_data.get('metadata', {}).get('git', {}).get('init', False):
                print(f"📦 Initializing git repository...")
                self._init_git(project_path, project_data)
            
            # Save project configuration
            self.interactive_setup.save_config(project_data, project_path)
            
            # Final success message
            print(f"\n✅ Project '{project_name}' created successfully!")
            print(f"📍 Location: {project_path}")
            print(f"\n🎯 Next steps:")
            print(f"   1. cd {project_path}")
            print(f"   2. Review GLOBAL_RULES.md for project standards")
            print(f"   3. Check TASKS.md for your task list")
            print(f"   4. Start with: claude-code")
            
            return True
            
        except KeyboardInterrupt:
            print(f"\n❌ Project creation cancelled by user.")
            if project_path.exists():
                shutil.rmtree(project_path)
            return False
        except Exception as e:
            print(f"\n❌ Error creating project: {e}", file=sys.stderr)
            if project_path.exists():
                shutil.rmtree(project_path)
            return False
    
    def _create_directory_structure(self, project_path: Path, project_data: Dict[str, Any]):
        """Create the complete directory structure."""
        # Create root directory
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create module directories
        for module in project_data.get('modules', []):
            module_path = project_path / module['name']
            module_path.mkdir(exist_ok=True)
            (module_path / 'docs').mkdir(exist_ok=True)
            (module_path / '__init__.py').touch()
            
            # Add .gitkeep to docs directory
            (module_path / 'docs' / '.gitkeep').touch()
        
        # Create tests directory structure
        tests_path = project_path / 'tests'
        tests_path.mkdir(exist_ok=True)
        (tests_path / '__init__.py').touch()
        
        for module in project_data.get('modules', []):
            test_module_path = tests_path / module['name']
            test_module_path.mkdir(exist_ok=True)
            (test_module_path / '__init__.py').touch()
            
            # Create initial test file
            test_file = test_module_path / f'test_{module["name"]}.py'
            test_content = f'''"""Tests for {module['name']} module."""
import pytest


class Test{module['name'].title()}:
    """Test cases for {module['name']} functionality."""
    
    def test_placeholder(self):
        """Placeholder test - replace with actual tests."""
        # TODO: Implement actual tests following TDD
        assert True, "Replace this with real tests"
'''
            test_file.write_text(test_content)
        
        # Create .claude directory
        claude_path = project_path / '.claude'
        claude_path.mkdir(exist_ok=True)
        (claude_path / 'commands').mkdir(exist_ok=True)
        
        # Create other standard directories based on project type
        project_type = project_data['metadata'].get('project_type', 'custom')
        
        if project_type == 'web':
            (project_path / 'static').mkdir(exist_ok=True)
            (project_path / 'templates').mkdir(exist_ok=True)
        elif project_type == 'ml':
            (project_path / 'data').mkdir(exist_ok=True)
            (project_path / 'models').mkdir(exist_ok=True)
            (project_path / 'notebooks').mkdir(exist_ok=True)
    
    def _create_claude_integration(self, project_path: Path, project_data: Dict[str, Any]):
        """Create .claude directory with settings and custom commands."""
        claude_path = project_path / '.claude'
        
        # Create settings.json
        settings = self.templates.get_template('claude_settings', {})
        (claude_path / 'settings.json').write_text(settings)
        
        # Create custom commands
        commands_path = claude_path / 'commands'
        
        # Test command
        if 'test' in project_data['metadata'].get('commands', {}):
            test_cmd = self.templates.create_custom_command('test', project_data)
            if test_cmd:
                test_file = commands_path / 'test.py'
                test_file.write_text(test_cmd)
                test_file.chmod(0o755)
        
        # Build command
        if 'build' in project_data['metadata'].get('commands', {}):
            build_cmd = self.templates.create_custom_command('build', project_data)
            if build_cmd:
                build_file = commands_path / 'build.py'
                build_file.write_text(build_cmd)
                build_file.chmod(0o755)
        
        # Create .gitignore
        gitignore_context = {
            'project_specific_ignores': self.helpers.get_project_specific_ignores(project_data)
        }
        gitignore = self.templates.get_template('gitignore', gitignore_context)
        (project_path / '.gitignore').write_text(gitignore)
        
        # Create CLAUDE.local.md template
        from datetime import datetime
        local_claude = f"""# Local Claude Configuration for {project_data['project_name']}

This file contains developer-specific configurations and notes.
It is git-ignored and won't be shared with the team.

## Personal Notes
- Add your personal development notes here

## Local Environment
- Add local environment setup notes

## Custom Shortcuts
- Add your custom workflow shortcuts

Generated on: {datetime.now().isoformat()}
"""
        (project_path / 'CLAUDE.local.md').write_text(local_claude)
    
    def _init_git(self, project_path: Path, project_data: Dict[str, Any]):
        """Initialize git repository."""
        try:
            # Initialize repository
            subprocess.run(['git', 'init'], cwd=project_path, check=True, capture_output=True)
            
            # Set initial branch
            branch = project_data['metadata']['git'].get('initial_branch', 'main')
            subprocess.run(['git', 'checkout', '-b', branch], cwd=project_path, check=True, capture_output=True)
            
            # Add all files
            subprocess.run(['git', 'add', '.'], cwd=project_path, check=True, capture_output=True)
            
            # Create initial commit
            commit_msg = f"Initial commit: {project_data['project_name']} scaffolded with Claude Scaffold"
            subprocess.run(['git', 'commit', '-m', commit_msg], cwd=project_path, check=True, capture_output=True)
            
            print(f"   ✓ Git repository initialized on branch '{branch}'")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Git initialization failed: {e}")
        except FileNotFoundError:
            print(f"   ⚠️  Git not found. Please install git to use version control.")