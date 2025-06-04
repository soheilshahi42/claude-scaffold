from typing import Dict, List, Any
from .icons import icons


class Formatters:
    """Formatting utilities for project documentation."""
    
    def organize_tasks_by_module(self, tasks: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize tasks by their assigned module."""
        module_tasks = {}
        for task in tasks:
            module = task['module']
            if module not in module_tasks:
                module_tasks[module] = []
            module_tasks[module].append(task)
        return module_tasks
    
    def format_module_tasks(self, module_name: str, tasks: List[Dict]) -> str:
        """Format tasks for a specific module."""
        if not tasks:
            return "No tasks assigned to this module yet."
        
        formatted = []
        for i, task in enumerate(tasks, 1):
            formatted.append(f"### Task {i} – {task['title']}")
            formatted.append(f"**Priority**: {task.get('priority', 'medium')}")
            
            # Use Claude-enhanced details if available
            if 'details' in task:
                details = task['details']
                formatted.append(f"**Goal**: {details.get('goal', 'To be defined during research phase')}")
                
                # Add requirements if available
                if 'requirements' in details and details['requirements']:
                    formatted.append("\n**Requirements**:")
                    for req in details['requirements'][:3]:  # Show first 3
                        formatted.append(f"- {req}")
                
                # Add approach if available
                if 'approach' in details:
                    formatted.append(f"\n**Approach**: {details['approach']}")
            else:
                formatted.append(f"**Goal**: To be defined during research phase")
            
            formatted.append(f"\n**Research file**: docs/{self.slugify(task['title'])}.md")
            formatted.append(f"**Sub-tasks**: see TODO.md")
            formatted.append("")
        
        return '\n'.join(formatted)
    
    def format_tasks_by_module(self, project_data: Dict[str, Any]) -> str:
        """Format all tasks organized by module."""
        module_tasks = self.organize_tasks_by_module(project_data['tasks'])
        
        formatted = []
        for module in project_data['modules']:
            tasks = module_tasks.get(module['name'], [])
            formatted.append(f"\n### {module['name']} ({len(tasks)} tasks)")
            
            if tasks:
                for task in tasks:
                    priority_emoji = {
                        'high': f'{icons.ERROR}',
                        'medium': f'{icons.WARNING}', 
                        'low': f'{icons.SUCCESS}'
                    }.get(task.get('priority', 'medium'), f'{icons.INFO}')
                    formatted.append(f"- {priority_emoji} {task['title']} ← details in /{module['name']}/CLAUDE.md")
            else:
                formatted.append("- No tasks assigned")
        
        return '\n'.join(formatted)
    
    def format_project_rules(self, project_data: Dict) -> str:
        """Format project-specific rules."""
        all_rules = []
        
        if 'suggested' in project_data['rules']:
            all_rules.extend(project_data['rules']['suggested'])
        
        if 'custom' in project_data['rules']:
            all_rules.extend(project_data['rules']['custom'])
        
        if all_rules:
            return '\n'.join(f"- {rule}" for rule in all_rules)
        
        return "- No project-specific rules defined"
    
    def format_constraints(self, project_data: Dict) -> str:
        """Format technical constraints."""
        constraints = project_data.get('constraints', [])
        
        if constraints:
            return '\n'.join(f"- {constraint}" for constraint in constraints)
        
        return "- No specific constraints defined"
    
    def format_dependencies(self, dependencies: list) -> str:
        """Format dependencies list."""
        if not dependencies:
            return "- Standard library modules\n- Project core utilities"
        
        formatted = []
        for dep in dependencies:
            if isinstance(dep, dict):
                formatted.append(f"- {dep.get('name', 'Unknown')}: {dep.get('purpose', '')}")
            else:
                formatted.append(f"- {dep}")
        
        return '\n'.join(formatted)
    
    def format_examples(self, examples: list) -> str:
        """Format usage examples."""
        if not examples:
            return "# Actual usage examples will be added during implementation"
        
        formatted = []
        for example in examples:
            if isinstance(example, dict):
                formatted.append(f"# {example.get('description', 'Example')}")
                formatted.append(example.get('code', '# Code here'))
                formatted.append("")
            else:
                formatted.append(str(example))
        
        return '\n'.join(formatted)
    
    def slugify(self, text: str) -> str:
        """Convert text to a valid filename."""
        return text.lower().replace(' ', '_').replace('-', '_').replace('/', '_')