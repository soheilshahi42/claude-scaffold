"""Claude-enhanced interactive setup that integrates AI at every step."""

import json
import questionary
from typing import Dict, List, Any, Optional
from datetime import datetime

from .claude_processor import ClaudeProcessor
from .project_config import ProjectConfig


class ClaudeInteractiveSetup:
    """Interactive setup with Claude enhancement at each step."""
    
    def __init__(self):
        self.processor = ClaudeProcessor()
        self.project_config = ProjectConfig()
        self.conversation_history = []
        
    def run(self, project_name: str, use_claude: bool = None) -> Dict[str, Any]:
        """Run Claude-enhanced interactive setup."""
        print(f"\n🎯 Setting up project: {project_name}")
        print("=" * 50)
        
        # Ask about Claude enhancement upfront
        if use_claude is None:
            use_claude = questionary.confirm(
                "\n🤖 Would you like to use Claude AI to enhance your project setup?",
                default=True
            ).ask()
        
        if use_claude:
            print("✨ Great! Claude will help optimize your project configuration at each step.")
        else:
            print("📋 Proceeding with standard setup (without AI enhancement).")
        
        # Initialize project data
        project_data = {
            'project_name': project_name,
            'timestamp': datetime.now().isoformat(),
            'version': '0.1.0',
            'enhanced_with_claude': use_claude,
            'metadata': {}
        }
        
        # Collect and enhance at each step
        project_data = self._collect_project_type(project_data, use_claude)
        project_data = self._collect_description(project_data, use_claude)
        project_data = self._collect_language(project_data, use_claude)
        project_data = self._collect_modules(project_data, use_claude)
        project_data = self._collect_tasks(project_data, use_claude)
        project_data = self._collect_rules(project_data, use_claude)
        project_data = self._collect_additional_config(project_data, use_claude)
        
        # Final review
        if not self._review_and_confirm(project_data):
            print("\n❌ Setup cancelled by user.")
            raise KeyboardInterrupt
        
        return project_data
    
    def _collect_project_type(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect project type with optional Claude enhancement."""
        print("\n📋 Project Type")
        
        # Show available types
        project_types = []
        for key, value in self.project_config.project_types.items():
            project_types.append({
                'name': f"{value['name']} - {value['description']}",
                'value': key
            })
        
        project_type = questionary.select(
            "Select your project type:",
            choices=project_types
        ).ask()
        
        project_data['metadata']['project_type'] = project_type
        project_data['metadata']['project_type_name'] = self.project_config.project_types[project_type]['name']
        
        # Claude enhancement
        if use_claude:
            enhanced = self._enhance_project_type(project_data)
            if enhanced:
                project_data['metadata'].update(enhanced)
        
        self._update_conversation_history("project_type", project_data)
        return project_data
    
    def _collect_description(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect project description with Claude enhancement."""
        print("\n📝 Project Description")
        
        # Get user's basic description
        description = questionary.text(
            "Brief project description:",
            default=f"A {project_data['metadata']['project_type_name'].lower()} built with Claude Scaffold"
        ).ask()
        
        project_data['metadata']['description'] = description
        
        # Claude enhancement
        if use_claude:
            enhanced_desc = self._enhance_description(project_data)
            if enhanced_desc:
                print(f"\n🤖 Claude suggests this enhanced description:")
                print(f"   {enhanced_desc}")
                
                use_enhanced = questionary.confirm(
                    "Use Claude's enhanced description?",
                    default=True
                ).ask()
                
                if use_enhanced:
                    project_data['metadata']['description'] = enhanced_desc
        
        self._update_conversation_history("description", project_data)
        return project_data
    
    def _collect_language(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect programming language."""
        print("\n💻 Programming Language")
        
        language = questionary.select(
            "Primary programming language:",
            choices=['Python', 'JavaScript', 'TypeScript', 'Both', 'Other']
        ).ask()
        
        project_data['metadata']['language'] = language
        
        # Claude can suggest style guides based on language and project type
        if use_claude and language in ['Python', 'Both']:
            suggested_style = self._get_suggested_style_guide(project_data)
            if suggested_style:
                print(f"\n🤖 Claude recommends: {suggested_style} for this project type")
                project_data['metadata']['suggested_style'] = suggested_style
        
        self._update_conversation_history("language", project_data)
        return project_data
    
    def _collect_modules(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect modules with Claude suggestions."""
        print("\n📦 Project Modules")
        
        modules = []
        suggested = self.project_config.project_types[project_data['metadata']['project_type']]['suggested_modules']
        
        if use_claude:
            # Get Claude's module suggestions based on all info so far
            claude_modules = self._get_claude_module_suggestions(project_data)
            if claude_modules:
                suggested = claude_modules
        
        # Show suggested modules
        if suggested:
            print(f"\nSuggested modules for {project_data['metadata']['project_type_name']}:")
            for module in suggested:
                print(f"   • {module}")
            
            use_suggested = questionary.confirm(
                "Would you like to use these suggested modules?",
                default=True
            ).ask()
            
            if use_suggested:
                modules = [{'name': m, 'description': f'{m.title()} module'} for m in suggested]
        
        # Allow adding custom modules
        while True:
            add_more = questionary.confirm(
                f"\n{'Add another module?' if modules else 'Add a module?'}",
                default=len(modules) == 0
            ).ask()
            
            if not add_more:
                break
            
            module_name = questionary.text(
                "Module name:",
                validate=lambda x: len(x) > 0 and x.replace('_', '').isalnum()
            ).ask()
            
            # Get Claude's description for the module if enabled
            if use_claude:
                module_desc = self._get_module_description(module_name, project_data)
            else:
                module_desc = questionary.text(
                    f"Description for {module_name} module:",
                    default=f"{module_name.title()} functionality"
                ).ask()
            
            modules.append({
                'name': module_name,
                'description': module_desc
            })
        
        project_data['modules'] = modules
        self._update_conversation_history("modules", project_data)
        return project_data
    
    def _collect_tasks(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect tasks with Claude assistance."""
        print("\n📋 Project Tasks")
        
        tasks = []
        
        if use_claude:
            # Get Claude's task suggestions based on modules and project info
            suggested_tasks = self._get_claude_task_suggestions(project_data)
            
            if suggested_tasks:
                print("\n🤖 Claude suggests these tasks:")
                for i, task in enumerate(suggested_tasks[:8], 1):
                    print(f"   {i}. {task['title']} ({task['module']})")
                
                selected = questionary.checkbox(
                    "Select tasks to include:",
                    choices=[f"{t['title']} ({t['module']})" for t in suggested_tasks]
                ).ask()
                
                for selection in selected:
                    # Parse the selection
                    for task in suggested_tasks:
                        if f"{task['title']} ({task['module']})" == selection:
                            tasks.append(task)
                            break
        
        # Allow adding custom tasks
        while True:
            add_more = questionary.confirm(
                f"\n{'Add another task?' if tasks else 'Add a task?'}",
                default=len(tasks) < 3
            ).ask()
            
            if not add_more:
                break
            
            task_title = questionary.text(
                "Task title:",
                validate=lambda x: len(x) > 0
            ).ask()
            
            # Let Claude suggest the best module
            if use_claude and len(project_data['modules']) > 1:
                suggested_module = self._suggest_module_for_task(task_title, project_data)
                module = questionary.select(
                    f"Which module should handle '{task_title}'?",
                    choices=[m['name'] for m in project_data['modules']],
                    default=suggested_module
                ).ask()
            else:
                module = questionary.select(
                    f"Which module should handle '{task_title}'?",
                    choices=[m['name'] for m in project_data['modules']]
                ).ask()
            
            priority = questionary.select(
                "Task priority:",
                choices=['high', 'medium', 'low'],
                default='medium'
            ).ask()
            
            tasks.append({
                'title': task_title,
                'module': module,
                'priority': priority
            })
        
        project_data['tasks'] = tasks
        self._update_conversation_history("tasks", project_data)
        return project_data
    
    def _collect_rules(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect project rules with Claude suggestions."""
        print("\n📏 Project Rules & Standards")
        
        rules = {'suggested': [], 'custom': []}
        
        if use_claude:
            # Get Claude's rule suggestions
            claude_rules = self._get_claude_rule_suggestions(project_data)
            if claude_rules:
                print("\n🤖 Claude recommends these project-specific rules:")
                for i, rule in enumerate(claude_rules[:10], 1):
                    print(f"   {i}. {rule}")
                
                selected = questionary.checkbox(
                    "Select rules to include:",
                    choices=claude_rules[:10],
                    default=claude_rules[:5]  # Pre-select first 5
                ).ask()
                
                rules['suggested'] = selected
        else:
            # Use standard suggestions
            suggested = self.project_config.project_types[project_data['metadata']['project_type']]['suggested_rules']
            if suggested:
                selected = questionary.checkbox(
                    "Select rules to include:",
                    choices=suggested,
                    default=suggested
                ).ask()
                rules['suggested'] = selected
        
        # Custom rules
        while questionary.confirm("\nAdd a custom rule?", default=False).ask():
            custom_rule = questionary.text(
                "Enter custom rule:",
                validate=lambda x: len(x) > 0
            ).ask()
            rules['custom'].append(custom_rule)
        
        project_data['rules'] = rules
        self._update_conversation_history("rules", project_data)
        return project_data
    
    def _collect_additional_config(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect additional configuration."""
        print("\n⚙️  Additional Configuration")
        
        # Get constraints
        if use_claude:
            constraints = self._get_claude_constraints(project_data)
        else:
            constraints = []
            if project_data['metadata']['language'] in ['Python', 'Both']:
                py_version = questionary.text("Minimum Python version:", default="3.8+").ask()
                constraints.append(f"Python {py_version}")
        
        project_data['constraints'] = constraints
        
        # Get build commands with Claude suggestions
        if use_claude:
            commands = self._get_claude_commands(project_data)
        else:
            commands = {}
            for cmd in ['install', 'test', 'build', 'dev']:
                cmd_value = questionary.text(f"{cmd.title()} command:").ask()
                if cmd_value:
                    commands[cmd] = cmd_value
        
        project_data['metadata']['commands'] = commands
        
        # Git setup
        git_init = questionary.confirm("Initialize git repository?", default=True).ask()
        if git_init:
            project_data['metadata']['git'] = {
                'init': True,
                'initial_branch': 'main'
            }
        
        self._update_conversation_history("config", project_data)
        return project_data
    
    def _review_and_confirm(self, project_data: Dict[str, Any]) -> bool:
        """Review configuration and confirm."""
        print("\n" + "=" * 60)
        print("📋 PROJECT CONFIGURATION SUMMARY")
        print("=" * 60)
        
        print(f"\n🎯 Project: {project_data['project_name']}")
        print(f"🤖 Claude Enhanced: {'Yes' if project_data.get('enhanced_with_claude') else 'No'}")
        print(f"📝 Type: {project_data['metadata']['project_type_name']}")
        print(f"💬 Description: {project_data['metadata']['description']}")
        print(f"💻 Language: {project_data['metadata']['language']}")
        
        print(f"\n📦 Modules ({len(project_data['modules'])})")
        for module in project_data['modules']:
            print(f"  • {module['name']} - {module['description']}")
        
        if project_data.get('tasks'):
            print(f"\n📋 Tasks ({len(project_data['tasks'])})")
            for task in project_data['tasks'][:5]:
                priority_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(task['priority'], '⚪')
                print(f"  {priority_icon} [{task['module']}] {task['title']}")
            if len(project_data['tasks']) > 5:
                print(f"  ... and {len(project_data['tasks']) - 5} more tasks")
        
        print("\n" + "=" * 60)
        
        return questionary.confirm("\nProceed with this configuration?", default=True).ask()
    
    # Claude enhancement methods
    def _enhance_project_type(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get Claude's insights about the project type."""
        prompt = f"""Based on this project setup:
- Project name: {project_data['project_name']}
- Type: {project_data['metadata']['project_type_name']}

Provide additional insights about this project type that would help with setup.
Return a JSON object with:
{{
    "key_considerations": ["list of important things to consider"],
    "common_patterns": ["common architectural patterns for this type"],
    "potential_challenges": ["typical challenges with this project type"]
}}"""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except:
            return {}
    
    def _enhance_description(self, project_data: Dict[str, Any]) -> str:
        """Get Claude to enhance the project description."""
        prompt = f"""Enhance this project description to be more comprehensive and clear:

Project: {project_data['project_name']}
Type: {project_data['metadata']['project_type_name']}
Original description: {project_data['metadata']['description']}

Provide a 2-3 sentence enhanced description that:
1. Clearly explains what the project does
2. Mentions key features or benefits
3. Indicates the target audience or use case

Return only the enhanced description text, no JSON."""
        
        try:
            return self.processor._call_claude(prompt).strip()
        except:
            return project_data['metadata']['description']
    
    def _get_suggested_style_guide(self, project_data: Dict[str, Any]) -> str:
        """Get Claude's style guide recommendation."""
        prompt = f"""For a {project_data['metadata']['project_type_name']} project using {project_data['metadata']['language']}, 
what Python style guide would you recommend? Consider the project type and common industry practices.
Return just the style guide name (e.g., "PEP 8", "Black", "Google Style Guide")."""
        
        try:
            return self.processor._call_claude(prompt).strip()
        except:
            return "PEP 8"
    
    def _get_claude_module_suggestions(self, project_data: Dict[str, Any]) -> List[str]:
        """Get Claude's module suggestions based on project info."""
        context = self._build_context(project_data)
        prompt = f"""{context}

Based on this project information, suggest the optimal module structure.
Consider the project type, description, and language.

Return a JSON array of module names that would be most appropriate.
Example: ["auth", "api", "database", "utils"]"""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except:
            return self.project_config.project_types[project_data['metadata']['project_type']]['suggested_modules']
    
    def _get_module_description(self, module_name: str, project_data: Dict[str, Any]) -> str:
        """Get Claude to describe what a module should do."""
        context = self._build_context(project_data)
        prompt = f"""{context}

For the module named "{module_name}", provide a clear, concise description of its purpose and responsibilities.
Return just the description text (one sentence)."""
        
        try:
            return self.processor._call_claude(prompt).strip()
        except:
            return f"{module_name.title()} functionality"
    
    def _get_claude_task_suggestions(self, project_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Claude's task suggestions."""
        context = self._build_context(project_data)
        prompt = f"""{context}

Suggest 8-10 specific development tasks for this project.
Consider the modules, project type, and description.
Assign each task to the most appropriate module.

Return a JSON array of task objects:
[
    {{"title": "task title", "module": "module_name", "priority": "high/medium/low"}},
    ...
]"""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except:
            return []
    
    def _suggest_module_for_task(self, task_title: str, project_data: Dict[str, Any]) -> str:
        """Get Claude to suggest which module should handle a task."""
        modules = [m['name'] for m in project_data['modules']]
        prompt = f"""Given this task: "{task_title}"
And these available modules: {', '.join(modules)}

Which module should handle this task? Return just the module name."""
        
        try:
            suggestion = self.processor._call_claude(prompt).strip()
            if suggestion in modules:
                return suggestion
        except:
            pass
        
        return modules[0]  # Default to first module
    
    def _get_claude_rule_suggestions(self, project_data: Dict[str, Any]) -> List[str]:
        """Get Claude's project-specific rule suggestions."""
        context = self._build_context(project_data)
        prompt = f"""{context}

Suggest 10 specific coding rules and best practices for this project.
Consider the project type, language, modules, and tasks.
Make them actionable and specific to this project's needs.

Return a JSON array of rule strings."""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except:
            return []
    
    def _get_claude_constraints(self, project_data: Dict[str, Any]) -> List[str]:
        """Get Claude's technical constraint suggestions."""
        context = self._build_context(project_data)
        prompt = f"""{context}

What technical constraints should this project have?
Consider dependencies, versions, deployment requirements, etc.

Return a JSON array of constraint strings (e.g., ["Python 3.8+", "PostgreSQL 12+"])."""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except:
            return []
    
    def _get_claude_commands(self, project_data: Dict[str, Any]) -> Dict[str, str]:
        """Get Claude's build command suggestions."""
        context = self._build_context(project_data)
        prompt = f"""{context}

Suggest appropriate commands for this project:
- install: Install dependencies
- test: Run tests
- build: Build the project
- dev: Start development server

Return a JSON object with command names as keys and commands as values.
Only include relevant commands for this project type."""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except:
            return {}
    
    def _build_context(self, project_data: Dict[str, Any]) -> str:
        """Build context string from conversation history."""
        context = f"""Project Setup Context:
- Name: {project_data['project_name']}
- Type: {project_data['metadata']['project_type_name']}
- Description: {project_data['metadata']['description']}
- Language: {project_data['metadata']['language']}"""
        
        if 'modules' in project_data and project_data['modules']:
            context += f"\n- Modules: {', '.join([m['name'] for m in project_data['modules']])}"
        
        if 'tasks' in project_data and project_data['tasks']:
            context += f"\n- Number of tasks defined: {len(project_data['tasks'])}"
        
        return context
    
    def _update_conversation_history(self, step: str, data: Dict[str, Any]):
        """Update conversation history for context building."""
        self.conversation_history.append({
            'step': step,
            'timestamp': datetime.now().isoformat(),
            'data': data.copy()
        })