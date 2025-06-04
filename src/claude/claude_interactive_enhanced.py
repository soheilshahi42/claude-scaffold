"""Enhanced Claude interactive setup with proper AI integration and refinement."""

import json
import questionary
from typing import Dict, List, Any, Optional
from datetime import datetime

from .claude_processor import ClaudeProcessor
from ..config.project_config import ProjectConfig
from ..utils.logger import get_logger
from ..utils.icons import icons


class EnhancedClaudeInteractiveSetup:
    """Interactive setup with proper Claude enhancement and refinement at each step."""
    
    def __init__(self, debug_mode: bool = False):
        self.processor = ClaudeProcessor(debug_mode=debug_mode)
        self.project_config = ProjectConfig()
        self.conversation_history = []
        self.logger = get_logger(debug_mode)
        
    def run(self, project_name: str, use_claude: bool = None) -> Dict[str, Any]:
        """Run enhanced Claude interactive setup."""
        print(f"\n{icons.CHEVRON} Setting up project: {project_name}")
        print("=" * 50)
        
        # Claude enhancement is now default when available
        if use_claude is None:
            use_claude = True
        
        if use_claude:
            print(f"{icons.STAR} Claude AI is enhancing your project configuration!")
            print(f"{icons.INFO} Tip: You can refine Claude's suggestions by providing feedback at each step.")
        else:
            print(f"{icons.DOCUMENT} Proceeding with standard setup (without AI enhancement).")
        
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
            print(f"\n{icons.ERROR} Setup cancelled by user.")
            raise KeyboardInterrupt
        
        return project_data
    
    def _refine_with_claude(self, current_value: Any, refinement_prompt: str, 
                           value_type: str = "text") -> Any:
        """Allow user to refine Claude's suggestion with feedback."""
        print(f"\n{icons.INFO} Would you like to refine this suggestion?")
        refine = questionary.confirm("Provide feedback to Claude?", default=False).ask()
        
        if not refine:
            return current_value
        
        feedback = questionary.text(
            "Your feedback (e.g., 'remove the part about X', 'add Y', 'make it shorter'):",
            multiline=True
        ).ask()
        
        if not feedback:
            return current_value
        
        # Build refinement prompt
        if value_type == "text":
            prompt = f"""{refinement_prompt}

Current version: {current_value}

User feedback: {feedback}

Provide an improved version based on the feedback. Return only the improved text."""
        elif value_type == "list":
            prompt = f"""{refinement_prompt}

Current items: {json.dumps(current_value)}

User feedback: {feedback}

Provide an improved list based on the feedback. Return a JSON array."""
        elif value_type == "dict":
            prompt = f"""{refinement_prompt}

Current data: {json.dumps(current_value)}

User feedback: {feedback}

Provide improved data based on the feedback. Return a JSON object."""
        
        try:
            response = self.processor._call_claude(prompt, expect_json=(value_type != "text"))
            if value_type == "text":
                return response.strip()
            else:
                return json.loads(response)
        except:
            print(f"{icons.WARNING} Could not process refinement, keeping original.")
            return current_value
    
    def _collect_project_type(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect project type with optional Claude enhancement."""
        print(f"\n{icons.DOCUMENT} Project Type")
        
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
        
        self._update_conversation_history("project_type", project_data)
        return project_data
    
    def _collect_description(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect project description with Claude enhancement and refinement."""
        print(f"\n{icons.DOCUMENT} Project Description")
        
        # Get user's basic description
        description = questionary.text(
            "Brief project description:",
            default=f"A {project_data['metadata']['project_type_name'].lower()} built with Claude Scaffold"
        ).ask()
        
        project_data['metadata']['description'] = description
        
        # Claude enhancement
        if use_claude:
            print(f"\n{icons.ROBOT} Enhancing description with Claude...")
            enhanced_desc = self._enhance_description(project_data)
            if enhanced_desc and enhanced_desc != description:
                print(f"\nClaude suggests this enhanced description:")
                print(f"   {enhanced_desc}")
                
                use_enhanced = questionary.confirm(
                    "Use Claude's enhanced description?",
                    default=True
                ).ask()
                
                if use_enhanced:
                    # Allow refinement
                    refined_desc = self._refine_with_claude(
                        enhanced_desc,
                        f"Refine this project description for {project_data['project_name']}",
                        "text"
                    )
                    project_data['metadata']['description'] = refined_desc
        
        self._update_conversation_history("description", project_data)
        return project_data
    
    def _collect_language(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect programming language."""
        print(f"\n{icons.CODE} Programming Language")
        
        # For React + Django, we should offer "Both" as default
        if "react" in project_data['metadata']['description'].lower() and \
           "django" in project_data['metadata']['description'].lower():
            default_choice = "Both"
        else:
            default_choice = "Python"
        
        language = questionary.select(
            "Primary programming language:",
            choices=['Python', 'JavaScript', 'TypeScript', 'Both', 'Other'],
            default=default_choice
        ).ask()
        
        project_data['metadata']['language'] = language
        
        self._update_conversation_history("language", project_data)
        return project_data
    
    def _collect_modules(self, project_data: Dict[str, Any], use_claude: bool) -> Dict[str, Any]:
        """Collect modules with Claude suggestions and refinement."""
        print(f"\n{icons.MODULE} Project Modules")
        
        modules = []
        
        if use_claude:
            # Get Claude's module suggestions based on all info so far
            print(f"\n{icons.ROBOT} Getting Claude's module suggestions...")
            claude_modules = self._get_claude_module_suggestions(project_data)
            if claude_modules:
                print("\nClaude suggests these modules:")
                for i, module in enumerate(claude_modules, 1):
                    print(f"   {i}. {module}")
                
                use_suggested = questionary.confirm(
                    "Use these suggested modules?",
                    default=True
                ).ask()
                
                if use_suggested:
                    # Allow refinement
                    refined_modules = self._refine_with_claude(
                        claude_modules,
                        f"Refine module structure for {project_data['project_name']}",
                        "list"
                    )
                    modules = [{'name': m, 'description': f'{m.title()} module'} for m in refined_modules]
                    
                    # Get descriptions for all modules concurrently
                    print(f"\n{icons.ROBOT} Generating module descriptions...")
                    module_names = [m['name'] for m in modules]
                    descriptions = self.processor.generate_module_descriptions_batch(
                        module_names, 
                        project_data
                    )
                    
                    # Update modules with descriptions
                    for module in modules:
                        if module['name'] in descriptions:
                            module['description'] = descriptions[module['name']]
        else:
            # Use default suggestions
            suggested = self.project_config.project_types[project_data['metadata']['project_type']]['suggested_modules']
            if suggested:
                print(f"\nSuggested modules for {project_data['metadata']['project_type_name']}:")
                for module in suggested:
                    print(f"   {icons.BULLET} {module}")
                
                use_suggested = questionary.confirm(
                    "Use these suggested modules?",
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
        """Collect tasks with Claude assistance and refinement."""
        print(f"\n{icons.TASK} Project Tasks")
        
        tasks = []
        
        if use_claude:
            # Get Claude's task suggestions
            print(f"\n{icons.ROBOT} Generating task suggestions based on your project...")
            suggested_tasks = self._get_claude_task_suggestions(project_data)
            
            if suggested_tasks:
                print("\nClaude suggests these tasks:")
                for i, task in enumerate(suggested_tasks[:10], 1):
                    priority_icon = icons.get_priority_icon(task.get('priority', 'medium'))
                    print(f"   {i}. {priority_icon} [{task['module']}] {task['title']}")
                
                use_suggested = questionary.confirm(
                    "Use these suggested tasks?",
                    default=True
                ).ask()
                
                if use_suggested:
                    # Allow refinement
                    refined_tasks = self._refine_with_claude(
                        suggested_tasks,
                        f"Refine task list for {project_data['project_name']}",
                        "list"
                    )
                    
                    # Let user select which tasks to include
                    from questionary import Choice
                    choices = []
                    for i, task in enumerate(refined_tasks[:15]):
                        priority_icon = icons.get_priority_icon(task.get('priority', 'medium'))
                        task_str = f"{priority_icon} [{task['module']}] {task['title']}"
                        # Pre-select first 8 tasks
                        choices.append(Choice(task_str, checked=(i < 8)))
                    
                    selected = questionary.checkbox(
                        "Select tasks to include:",
                        choices=choices
                    ).ask()
                    
                    # Map selections back to tasks
                    for selection in selected:
                        for task in refined_tasks:
                            priority_icon = icons.get_priority_icon(task.get('priority', 'medium'))
                            if f"{priority_icon} [{task['module']}] {task['title']}" == selection:
                                tasks.append(task)
                                break
        
        # Allow adding custom tasks
        while questionary.confirm(f"\n{'Add another task?' if tasks else 'Add a task?'}", default=len(tasks) < 3).ask():
            task_title = questionary.text("Task title:", validate=lambda x: len(x) > 0).ask()
            
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
        """Collect project rules with Claude suggestions and refinement."""
        print(f"\n{icons.RULE} Project Rules & Standards")
        
        rules = {'suggested': [], 'custom': []}
        
        if use_claude:
            # Get Claude's rule suggestions
            print(f"\n{icons.ROBOT} Generating project-specific rules...")
            claude_rules = self._get_claude_rule_suggestions(project_data)
            
            if claude_rules:
                print("\nClaude recommends these project-specific rules:")
                for i, rule in enumerate(claude_rules[:12], 1):
                    print(f"   {i}. {rule}")
                
                use_suggested = questionary.confirm(
                    "Use these suggested rules?",
                    default=True
                ).ask()
                
                if use_suggested:
                    # Allow refinement
                    refined_rules = self._refine_with_claude(
                        claude_rules,
                        f"Refine project rules for {project_data['project_name']}",
                        "list"
                    )
                    
                    # Let user select which rules to include
                    from questionary import Choice
                    rule_choices = []
                    for i, rule in enumerate(refined_rules[:15]):
                        # Pre-select first 8 rules
                        rule_choices.append(Choice(rule, checked=(i < 8)))
                    
                    selected = questionary.checkbox(
                        "Select rules to include:",
                        choices=rule_choices
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
        """Collect additional configuration with Claude assistance."""
        print(f"\n{icons.CONFIG} Additional Configuration")
        
        # Get constraints
        if use_claude:
            print(f"\n{icons.ROBOT} Determining technical constraints...")
            constraints = self._get_claude_constraints(project_data)
            if constraints:
                print("\nClaude suggests these constraints:")
                for constraint in constraints:
                    print(f"   {icons.BULLET} {constraint}")
                
                use_constraints = questionary.confirm(
                    "Use these constraints?",
                    default=True
                ).ask()
                
                if use_constraints:
                    # Allow refinement
                    constraints = self._refine_with_claude(
                        constraints,
                        f"Refine technical constraints for {project_data['project_name']}",
                        "list"
                    )
                else:
                    constraints = []
        else:
            constraints = []
            if project_data['metadata']['language'] in ['Python', 'Both']:
                py_version = questionary.text("Minimum Python version:", default="3.8+").ask()
                constraints.append(f"Python {py_version}")
        
        project_data['constraints'] = constraints
        
        # Get build commands
        if use_claude:
            print(f"\n{icons.ROBOT} Generating build commands...")
            commands = self._get_claude_commands(project_data)
            if commands:
                print("\nClaude suggests these commands:")
                for cmd, value in commands.items():
                    print(f"   {cmd}: {value}")
                
                use_commands = questionary.confirm(
                    "Use these commands?",
                    default=True
                ).ask()
                
                if not use_commands:
                    commands = {}
        else:
            commands = {}
        
        # Allow manual command entry/override
        for cmd in ['install', 'test', 'build', 'dev', 'lint']:
            if cmd not in commands:
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
    
    # Claude enhancement methods with proper implementation
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
            return self.processor._call_claude(prompt, expect_json=False).strip()
        except Exception as e:
            print(f"{icons.WARNING} Could not enhance description: {e}")
            return project_data['metadata']['description']
    
    def _get_claude_module_suggestions(self, project_data: Dict[str, Any]) -> List[str]:
        """Get Claude's module suggestions based on project info."""
        context = self._build_context(project_data)
        prompt = f"""{context}

Based on this project information, suggest the optimal module structure.
Consider the project type, description, and language.
Think about appropriate separation of concerns, API design, and common features for this type of project.

Return a JSON array of module names that would be most appropriate."""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except Exception as e:
            print(f"{icons.WARNING} Using default modules: {e}")
            return self.project_config.project_types[project_data['metadata']['project_type']]['suggested_modules']
    
    def _get_module_description(self, module_name: str, project_data: Dict[str, Any]) -> str:
        """Get Claude to describe what a module should do."""
        context = self._build_context(project_data)
        prompt = f"""{context}

For the module named "{module_name}", provide a clear, concise description of its purpose and responsibilities.
Consider the project context and how this module fits into the architecture.
Return just the description text (one sentence)."""
        
        try:
            return self.processor._call_claude(prompt, expect_json=False).strip()
        except:
            return f"{module_name.title()} functionality"
    
    def _get_claude_task_suggestions(self, project_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Claude's task suggestions."""
        self.logger.info("Getting Claude task suggestions", 
                        {'project_name': project_data['project_name'],
                         'modules': [m['name'] for m in project_data.get('modules', [])]})
        
        context = self._build_context(project_data)
        prompt = f"""{context}

Suggest 10-15 specific development tasks for this project.
Consider the modules, project type, and description.
Based on the project type and language, include appropriate tasks for all major components.
Assign each task to the most appropriate module.
Mix priorities to show what's most important.

Return a JSON array of task objects:
[
    {{"title": "Set up Django REST framework", "module": "backend", "priority": "high"}},
    {{"title": "Create React app with TypeScript", "module": "frontend", "priority": "high"}},
    ...
]"""
        
        try:
            self.logger.debug("Calling Claude for task suggestions")
            response = self.processor._call_claude(prompt)
            self.logger.debug("Claude response received", {'response_length': len(response)})
            
            tasks = json.loads(response)
            self.logger.info(f"Successfully parsed {len(tasks)} tasks from Claude")
            return tasks
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse Claude response as JSON", e, 
                            {'response_preview': response[:200] if 'response' in locals() else 'N/A'})
            print(f"{icons.WARNING} Could not generate tasks: {e}")
            return []
        except Exception as e:
            self.logger.error("Error getting Claude task suggestions", e)
            print(f"{icons.WARNING} Could not generate tasks: {e}")
            return []
    
    def _suggest_module_for_task(self, task_title: str, project_data: Dict[str, Any]) -> str:
        """Get Claude to suggest which module should handle a task."""
        modules = [m['name'] for m in project_data['modules']]
        prompt = f"""Given this task: "{task_title}"
And these available modules: {', '.join(modules)}

Which module should handle this task? Return just the module name."""
        
        try:
            suggestion = self.processor._call_claude(prompt, expect_json=False).strip()
            if suggestion in modules:
                return suggestion
        except:
            pass
        
        return modules[0]  # Default to first module
    
    def _get_claude_rule_suggestions(self, project_data: Dict[str, Any]) -> List[str]:
        """Get Claude's project-specific rule suggestions."""
        context = self._build_context(project_data)
        prompt = f"""{context}

Suggest 12-15 specific coding rules and best practices for this project.
Consider the project type, language, modules, and tasks.
Make them actionable and specific to this project's needs.
Include rules for all major components based on the chosen technology stack.
Consider security, performance, testing, and code organization.

Return a JSON array of rule strings."""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except Exception as e:
            print(f"{icons.WARNING} Could not generate rules: {e}")
            return []
    
    def _get_claude_constraints(self, project_data: Dict[str, Any]) -> List[str]:
        """Get Claude's technical constraint suggestions."""
        context = self._build_context(project_data)
        prompt = f"""{context}

What technical constraints should this project have?
Consider dependencies, versions, deployment requirements, etc.
Based on the project type and language, think about appropriate runtime versions, database requirements, and deployment constraints.

Return a JSON array of constraint strings."""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except Exception as e:
            print(f"{icons.WARNING} Could not generate constraints: {e}")
            return []
    
    def _get_claude_commands(self, project_data: Dict[str, Any]) -> Dict[str, str]:
        """Get Claude's build command suggestions."""
        context = self._build_context(project_data)
        prompt = f"""{context}

Suggest appropriate commands for this project:
- install: Install all dependencies
- test: Run all tests
- build: Build the project for production
- dev: Start development servers
- lint: Run linters

Based on the project type and language, suggest commands that handle all project components.

Return a JSON object with command names as keys and commands as values.
Only include relevant commands for this project type."""
        
        try:
            response = self.processor._call_claude(prompt)
            return json.loads(response)
        except Exception as e:
            print(f"{icons.WARNING} Could not generate commands: {e}")
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
    
    def _review_and_confirm(self, project_data: Dict[str, Any]) -> bool:
        """Review configuration and confirm."""
        print("\n" + "=" * 60)
        print(f"{icons.DOCUMENT} PROJECT CONFIGURATION SUMMARY")
        print("=" * 60)
        
        print(f"\n{icons.CHEVRON} Project: {project_data['project_name']}")
        print(f"{icons.ROBOT} Claude Enhanced: {'Yes' if project_data.get('enhanced_with_claude') else 'No'}")
        print(f"{icons.DOCUMENT} Type: {project_data['metadata']['project_type_name']}")
        print(f"{icons.INFO} Description: {project_data['metadata']['description']}")
        print(f"{icons.CODE} Language: {project_data['metadata']['language']}")
        
        print(f"\n{icons.MODULE} Modules ({len(project_data['modules'])})")
        for module in project_data['modules']:
            print(f"  {icons.BULLET} {module['name']} - {module['description']}")
        
        if project_data.get('tasks'):
            print(f"\n{icons.TASK} Tasks ({len(project_data['tasks'])})")
            for task in project_data['tasks'][:5]:
                priority_icon = icons.get_priority_icon(task['priority'])
                print(f"  {priority_icon} [{task['module']}] {task['title']}")
            if len(project_data['tasks']) > 5:
                print(f"  ... and {len(project_data['tasks']) - 5} more tasks")
        
        # Rules
        total_rules = len(project_data['rules']['suggested']) + len(project_data['rules']['custom'])
        if total_rules:
            print(f"\n{icons.RULE} Rules ({total_rules})")
            for rule in (project_data['rules']['suggested'] + project_data['rules']['custom'])[:3]:
                print(f"  {icons.BULLET} {rule}")
            if total_rules > 3:
                print(f"  ... and {total_rules - 3} more rules")
        
        # Constraints
        if project_data.get('constraints'):
            print(f"\n{icons.CONFIG} Constraints")
            for constraint in project_data['constraints']:
                print(f"  {icons.BULLET} {constraint}")
        
        # Commands
        if project_data['metadata'].get('commands'):
            print(f"\n{icons.BUILD} Commands")
            for cmd_type, cmd in project_data['metadata']['commands'].items():
                if cmd:
                    print(f"  {cmd_type}: {cmd}")
        
        print("\n" + "=" * 60)
        
        return questionary.confirm(
            "\nProceed with this configuration?",
            default=True
        ).ask()