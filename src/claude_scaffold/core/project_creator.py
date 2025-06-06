import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from ..interactive.enhanced_setup import EnhancedInteractiveSetup
from ..interactive.interactive_setup import InteractiveSetup
from ..templates.templates import ProjectTemplates
from ..utils.icons import icons
from ..utils.logger import get_logger
from ..utils.project_helpers import ProjectHelpers
from ..utils.ui_manager import ui_manager
from .documentation_generator import DocumentationGenerator


class ProjectCreator:
    """Handles the main project creation workflow."""

    def __init__(self, debug_mode: bool = False):
        self.templates = ProjectTemplates()
        self.interactive_setup = InteractiveSetup(debug_mode=debug_mode)
        self.enhanced_setup = None  # Created on demand
        self.doc_generator = DocumentationGenerator()
        self.helpers = ProjectHelpers()
        self.logger = get_logger(debug_mode)
        from ..config.project_config import ProjectConfig
        self.project_config = ProjectConfig()

    def check_claude_available(self) -> bool:
        """Check if Claude CLI is available."""
        try:
            result = subprocess.run(["claude", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{icons.SUCCESS} Claude CLI detected - intelligent configuration available!")
                return True
        except FileNotFoundError:
            pass

        print(f"{icons.WARNING} Claude CLI not found - using standard configuration")
        print(
            "   Install Claude CLI for intelligent project setup: https://github.com/anthropics/claude-code"
        )
        return False

    def create_project(
        self,
        project_name: str,
        project_path: Optional[Path] = None,
        force: bool = False,
        interactive: bool = True,
        enhanced: bool = False,
        config_file: Optional[Path] = None,
    ) -> bool:
        """Create a new Claude Scaffold project."""
        if project_path is None:
            project_path = Path.cwd() / project_name

        # Check if project exists
        if project_path.exists() and not force:
            print(
                f"{icons.ERROR} Error: Project '{project_name}' already exists.",
                file=sys.stderr,
            )
            print(
                "   Use --force to overwrite or choose a different name.",
                file=sys.stderr,
            )
            return False

        if project_path.exists() and force:
            print(f"{icons.WARNING} Removing existing project at {project_path}")
            shutil.rmtree(project_path)

        try:
            # Handle interactive setup separately to avoid terminal conflicts
            if interactive:
                print(f"\n{icons.PROGRESS} Starting interactive setup...")
                if enhanced:
                    # Use enhanced setup with deep discovery
                    if self.enhanced_setup is None:
                        self.enhanced_setup = EnhancedInteractiveSetup(
                            config_file=str(config_file) if config_file else None
                        )
                    project_data = self.enhanced_setup.run()
                else:
                    # Check if Claude is available
                    use_claude = self.check_claude_available()
                    project_data = self.interactive_setup.run(project_name, use_claude=use_claude)
                print(f"{icons.SUCCESS} Interactive setup completed\n")
            else:
                # Use config file if provided, otherwise minimal defaults
                if config_file and config_file.exists():
                    import yaml
                    from datetime import datetime
                    with open(config_file, 'r') as f:
                        project_data = yaml.safe_load(f)
                    # Ensure project_name is set
                    project_data['project_name'] = project_name
                    # Add required metadata if missing
                    if 'metadata' not in project_data:
                        project_data['metadata'] = {}
                    if 'timestamp' not in project_data:
                        project_data['timestamp'] = datetime.now().isoformat()
                    if 'version' not in project_data:
                        project_data['version'] = '0.1.0'
                    # Set project type metadata
                    project_type = project_data.get('project_type', 'custom')
                    project_data['metadata']['project_type'] = project_type
                    project_data['metadata']['project_type_name'] = self.project_config.project_types.get(
                        project_type, {}).get('name', 'Custom Project')
                    if 'description' not in project_data['metadata']:
                        project_data['metadata']['description'] = project_data.get(
                            'description', f'{project_name} - A Claude Scaffold project')
                else:
                    project_data = self.helpers.get_default_project_data(project_name)

            # Determine total steps based on configuration
            total_steps = 4  # Base steps: structure, docs, claude, config
            if project_data.get("metadata", {}).get("git", {}).get("init", False):
                total_steps += 1

            # Now run the rest with progress tracking
            with ui_manager.step_progress(
                f"Creating project '{project_name}'", total_steps=total_steps
            ) as progress:
                # Project structure and setup steps follow

                # Create project structure
                progress.update("Creating directory structure")
                self._create_directory_structure(project_path, project_data)

                # Generate all documentation
                progress.update("Generating documentation")
                self.doc_generator.generate_documentation(project_path, project_data)

                # Create .claude directory and files
                progress.update("Setting up Claude Code integration")
                self._create_claude_integration(project_path, project_data)

                # Initialize git if requested
                if project_data.get("metadata", {}).get("git", {}).get("init", False):
                    progress.update("Initializing git repository")
                    self._init_git(project_path, project_data)

                # Save project configuration
                progress.update("Saving project configuration")
                self.interactive_setup.save_config(project_data, project_path)

                progress.complete(f"Project '{project_name}' created successfully!")

            # Show summary
            summary_items = [
                {
                    "Component": "Modules",
                    "Count": len(project_data.get("modules", [])),
                    "Status": "completed",
                },
                {
                    "Component": "Tasks",
                    "Count": len(project_data.get("tasks", [])),
                    "Status": "completed",
                },
                {
                    "Component": "Documentation Files",
                    "Count": sum(1 for _ in project_path.rglob("*.md")),
                    "Status": "completed",
                },
                {
                    "Component": "Test Files",
                    "Count": sum(1 for _ in project_path.rglob("test_*.py")),
                    "Status": "completed",
                },
            ]

            ui_manager.show_summary("Project Creation Summary", summary_items)

            # Final success message
            print(f"\n{icons.SUCCESS} Project '{project_name}' created successfully!")
            print(f"{icons.ARROW_RIGHT} Location: {project_path}")
            print(f"\n{icons.CHEVRON} Next steps:")
            print(f"   1. cd {project_path}")
            print("   2. Review GLOBAL_RULES.md for project standards")
            print("   3. Check TASKS.md for your task list")
            print("   4. Start with: claude-code")

            # Show operation summary with timings
            ui_manager.show_operation_summary()

            return True

        except KeyboardInterrupt:
            print(f"\n{icons.ERROR} Project creation cancelled by user.")
            if project_path.exists():
                shutil.rmtree(project_path)
            return False
        except Exception as e:
            print(f"\n{icons.ERROR} Error creating project: {e}", file=sys.stderr)
            if project_path.exists():
                shutil.rmtree(project_path)
            return False

    def _create_directory_structure(self, project_path: Path, project_data: Dict[str, Any]):
        """Create the complete directory structure."""
        # Create root directory
        project_path.mkdir(parents=True, exist_ok=True)

        # Create module directories
        for module in project_data.get("modules", []):
            module_path = project_path / module["name"]
            module_path.mkdir(parents=True, exist_ok=True)
            (module_path / "docs").mkdir(exist_ok=True)
            (module_path / "__init__.py").touch()

            # Add .gitkeep to docs directory
            (module_path / "docs" / ".gitkeep").touch()

        # Create tests directory structure
        tests_path = project_path / "tests"
        tests_path.mkdir(exist_ok=True)
        (tests_path / "__init__.py").touch()

        for module in project_data.get("modules", []):
            test_module_path = tests_path / module["name"]
            test_module_path.mkdir(parents=True, exist_ok=True)
            (test_module_path / "__init__.py").touch()

            # Create initial test file
            # Extract the last part of the module name for the test file name
            module_base_name = module["name"].split("/")[-1]
            test_file = test_module_path / f'test_{module_base_name}.py'
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
        claude_path = project_path / ".claude"
        claude_path.mkdir(exist_ok=True)
        (claude_path / "commands").mkdir(exist_ok=True)

        # Create other standard directories based on project type
        project_type = project_data["metadata"].get("project_type", "custom")

        if project_type == "web":
            (project_path / "static").mkdir(exist_ok=True)
            (project_path / "templates").mkdir(exist_ok=True)
        elif project_type == "ml":
            (project_path / "data").mkdir(exist_ok=True)
            (project_path / "models").mkdir(exist_ok=True)
            (project_path / "notebooks").mkdir(exist_ok=True)

    def _create_claude_integration(self, project_path: Path, project_data: Dict[str, Any]):
        """Create .claude directory with settings and custom commands."""
        claude_path = project_path / ".claude"

        # Create settings.json
        settings = self.templates.get_template("claude_settings", {})
        (claude_path / "settings.json").write_text(settings)

        # Create custom Claude Code commands (Markdown files)
        commands_path = claude_path / "commands"

        # Get command templates
        from ..templates.template_commands import CommandTemplates

        command_templates = CommandTemplates.get_templates()

        # Create all command files
        for cmd_name, cmd_content in command_templates.items():
            # Replace any template variables
            if cmd_name == "test.md" and "test" in project_data["metadata"].get("commands", {}):
                cmd_content = cmd_content.replace(
                    "{test_command}", project_data["metadata"]["commands"]["test"]
                )

            cmd_file = commands_path / cmd_name
            cmd_file.write_text(cmd_content)

        # Create .gitignore
        gitignore_context = {
            "project_specific_ignores": self.helpers.get_project_specific_ignores(project_data)
        }
        gitignore = self.templates.get_template("gitignore", gitignore_context)
        (project_path / ".gitignore").write_text(gitignore)

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
        (project_path / "CLAUDE.local.md").write_text(local_claude)

    def _init_git(self, project_path: Path, project_data: Dict[str, Any]):
        """Initialize git repository."""
        try:
            # Initialize repository
            subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True)

            # Set initial branch
            branch = project_data["metadata"]["git"].get("initial_branch", "main")
            subprocess.run(
                ["git", "checkout", "-b", branch],
                cwd=project_path,
                check=True,
                capture_output=True,
            )

            # Add all files
            subprocess.run(
                ["git", "add", "."],
                cwd=project_path,
                check=True,
                capture_output=True,
            )

            # Create initial commit
            commit_msg = (
                f"Initial commit: {project_data['project_name']} scaffolded with Claude Scaffold"
            )
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=project_path,
                check=True,
                capture_output=True,
            )

            print(f"   {icons.SUCCESS} Git repository initialized on branch '{branch}'")

        except subprocess.CalledProcessError as e:
            print(f"   {icons.WARNING} Git initialization failed: {e}")
        except FileNotFoundError:
            print(f"   {icons.WARNING} Git not found. Please install git to use version control.")
