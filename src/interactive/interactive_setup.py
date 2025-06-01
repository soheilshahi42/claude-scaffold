"""Main interactive setup module."""

import questionary
from typing import Dict, Optional, Any
import yaml
from pathlib import Path
import textwrap
from datetime import datetime

from ..config.project_config import ProjectConfig
from .interactive_collectors import InteractiveCollectors
from ..claude.claude_enhancer import ClaudeEnhancedSetup
from ..claude.claude_interactive_enhanced import EnhancedClaudeInteractiveSetup
from ..utils.logger import get_logger
import subprocess


class InteractiveSetup:
    """Enhanced interactive setup with questionary and Claude integration."""
    
    def __init__(self, debug_mode: bool = False):
        self.project_config = ProjectConfig()
        self.collectors = InteractiveCollectors(self.project_config)
        # Make properties available for backward compatibility
        self.project_types = self.project_config.project_types
        self.style_guides = self.project_config.style_guides
        self.test_frameworks = self.project_config.test_frameworks
        self.logger = get_logger(debug_mode)
        self.debug_mode = debug_mode
    
    def _check_claude_available(self) -> bool:
        """Check if Claude CLI is available."""
        try:
            result = subprocess.run(['claude', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def run(self, project_name: str, use_claude: bool = True) -> Dict[str, Any]:
        """Run the interactive setup process."""
        # First, check if Claude is available
        claude_available = self._check_claude_available()
        
        if claude_available and use_claude:
            # Use the new enhanced Claude interactive setup
            claude_setup = EnhancedClaudeInteractiveSetup(debug_mode=self.debug_mode)
            return claude_setup.run(project_name, use_claude=True)
        
        # Fall back to standard setup
        print(f"\n🎯 Setting up project: {project_name}")
        print("=" * 50)
        
        if not claude_available:
            print("⚠️  Claude CLI not detected. Proceeding with standard setup.")
        
        # Initialize project data
        project_data = {
            'project_name': project_name,
            'timestamp': datetime.now().isoformat(),
            'version': '0.1.0',
            'modules': [],
            'tasks': [],
            'rules': {'suggested': [], 'custom': []},
            'constraints': [],
            'metadata': {}
        }
        
        try:
            # Step 1: Collect basic project information
            project_data = self._collect_project_info(project_data)
            
            # Step 2: Collect modules
            project_data['modules'] = self.collectors.collect_modules(project_data)
            
            # Step 3: Collect tasks
            project_data['tasks'] = self.collectors.collect_tasks(
                project_data, 
                project_data['modules']
            )
            
            # Step 4: Collect rules
            project_data['rules'] = self.collectors.collect_rules(project_data)
            
            # Step 5: Additional configuration
            project_data = self.collectors.collect_additional_config(project_data)
            
            # Step 6: Review and confirm
            if not self._review_and_confirm(project_data):
                print("\n❌ Setup cancelled by user.")
                raise KeyboardInterrupt
            
            return project_data
            
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"\n❌ Error during interactive setup: {e}")
            raise
    
    def _collect_project_info(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect basic project information."""
        # Project type
        print("\n📋 Project Type")
        project_type_choices = []
        for key, value in self.project_types.items():
            project_type_choices.append({
                'name': f"{value['name']} - {value['description']}",
                'value': key
            })
        
        project_type = questionary.select(
            "Select your project type:",
            choices=project_type_choices
        ).ask()
        
        project_data['metadata']['project_type'] = project_type
        project_data['metadata']['project_type_name'] = self.project_types[project_type]['name']
        
        # Project description
        print(f"\n📝 Project Description")
        description = questionary.text(
            "Brief project description:",
            default=f"A {self.project_types[project_type]['name'].lower()} built with Claude Scaffold"
        ).ask()
        
        project_data['metadata']['description'] = description
        
        # Programming language
        print("\n💻 Programming Language")
        language = questionary.select(
            "Primary programming language:",
            choices=['Python', 'JavaScript', 'TypeScript', 'Both', 'Other']
        ).ask()
        
        project_data['metadata']['language'] = language
        
        # Style guide
        print("\n🎨 Code Style")
        if language in ['Python', 'Both']:
            style_choices = []
            for key, value in self.style_guides.items():
                style_choices.append({
                    'name': value,
                    'value': key
                })
            
            style_guide = questionary.select(
                "Select style guide:",
                choices=style_choices
            ).ask()
            
            project_data['metadata']['style_guide'] = style_guide
        else:
            project_data['metadata']['style_guide'] = 'custom'
        
        # Test framework
        print("\n🧪 Testing Framework")
        test_framework = self.project_types[project_type]['test_framework']
        
        use_default = questionary.confirm(
            f"Use {test_framework} for testing?",
            default=True
        ).ask()
        
        if not use_default:
            test_choices = []
            for key, value in self.test_frameworks.items():
                test_choices.append({
                    'name': value,
                    'value': key
                })
            
            test_framework = questionary.select(
                "Select testing framework:",
                choices=test_choices
            ).ask()
        
        project_data['metadata']['test_framework'] = test_framework
        
        return project_data
    
    def _review_and_confirm(self, project_data: Dict[str, Any]) -> bool:
        """Review configuration and confirm."""
        print("\n" + "=" * 60)
        print("📋 PROJECT CONFIGURATION SUMMARY")
        print("=" * 60)
        
        # Basic info
        print(f"\n🎯 Project: {project_data['project_name']}")
        print(f"📝 Type: {project_data['metadata']['project_type_name']}")
        print(f"💬 Description: {project_data['metadata']['description']}")
        print(f"💻 Language: {project_data['metadata']['language']}")
        print(f"🎨 Style: {self.style_guides.get(project_data['metadata'].get('style_guide', 'custom'), 'Custom')}")
        print(f"🧪 Testing: {project_data['metadata'].get('test_framework', 'pytest')}")
        
        # Modules
        print(f"\n📦 Modules ({len(project_data['modules'])})")
        for module in project_data['modules']:
            icon = "  ✨" if module['type'] == 'suggested' else "  ➕"
            print(f"{icon} {module['name']} - {module['description']}")
        
        # Tasks
        if project_data['tasks']:
            print(f"\n📋 Tasks ({len(project_data['tasks'])})")
            for task in project_data['tasks'][:5]:
                priority_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(task['priority'], '⚪')
                print(f"  {priority_icon} [{task['module']}] {task['title']}")
            if len(project_data['tasks']) > 5:
                print(f"  ... and {len(project_data['tasks']) - 5} more tasks")
        
        # Rules
        total_rules = len(project_data['rules']['suggested']) + len(project_data['rules']['custom'])
        if total_rules:
            print(f"\n📏 Rules ({total_rules})")
            for rule in (project_data['rules']['suggested'] + project_data['rules']['custom'])[:3]:
                print(f"  • {rule}")
            if total_rules > 3:
                print(f"  ... and {total_rules - 3} more rules")
        
        # Commands
        if project_data['metadata'].get('commands'):
            print(f"\n🔨 Commands")
            for cmd_type, cmd in project_data['metadata']['commands'].items():
                if cmd:
                    print(f"  {cmd_type}: {cmd}")
        
        print("\n" + "=" * 60)
        
        return questionary.confirm(
            "\nProceed with this configuration?",
            default=True
        ).ask()
    
    def save_config(self, project_data: Dict[str, Any], path: Path):
        """Save project configuration to file."""
        config_path = path / '.claude' / 'project_config.yaml'
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, 'w') as f:
            yaml.dump(project_data, f, default_flow_style=False, sort_keys=False)
    
    def load_config(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load project configuration from file."""
        config_path = path / '.claude' / 'project_config.yaml'
        
        if not config_path.exists():
            return None
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)