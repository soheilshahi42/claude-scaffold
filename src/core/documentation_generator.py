from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from ..templates.templates import ProjectTemplates
from ..utils.formatters import Formatters
from ..utils.project_helpers import ProjectHelpers
from ..utils.icons import icons


class DocumentationGenerator:
    """Handles all documentation generation for the project."""
    
    def __init__(self):
        self.templates = ProjectTemplates()
        self.formatters = Formatters()
        self.helpers = ProjectHelpers()
    
    def generate_documentation(self, project_path: Path, project_data: Dict[str, Any]):
        """Generate all documentation files."""
        # Prepare context for templates
        context = self.helpers.prepare_template_context(project_data)
        
        # Generate root CLAUDE.md
        root_claude = self.templates.get_template('root_claude', context)
        (project_path / 'CLAUDE.md').write_text(root_claude)
        
        # Generate GLOBAL_RULES.md
        global_rules = self.templates.get_template('global_rules', context)
        (project_path / 'GLOBAL_RULES.md').write_text(global_rules)
        
        # Generate TASKS.md
        tasks_md = self.templates.get_template('tasks_md', context)
        (project_path / 'TASKS.md').write_text(tasks_md)
        
        # Generate root TODO.md
        root_todos = []
        for module in project_data.get('modules', []):
            root_todos.append(f"- [ ] Complete all tasks in {module['name']} module")
        
        self.create_todo_file(
            project_path / 'TODO.md',
            project_data['project_name'],
            "the entire project",
            root_todos
        )
        
        # Generate module documentation
        module_tasks = self.formatters.organize_tasks_by_module(project_data['tasks'])
        
        for module in project_data.get('modules', []):
            module_path = project_path / module['name']
            
            # Prepare module-specific context
            module_context = context.copy()
            
            # Use Claude-enhanced documentation if available
            if 'documentation' in module:
                claude_docs = module['documentation']
                module_context.update({
                    'module_name': module['name'],
                    'module_description': module['description'],
                    'module_responsibilities': claude_docs.get('responsibilities', self.helpers.get_module_responsibilities(module, project_data)),
                    'public_api': claude_docs.get('public_api', 'To be defined during implementation'),
                    'internal_architecture': claude_docs.get('architecture', 'To be defined during implementation'),
                    'dependencies': self.formatters.format_dependencies(claude_docs.get('dependencies', [])),
                    'naming_conventions': self.helpers.get_naming_conventions(project_data),
                    'file_organization': self.helpers.get_file_organization(module, project_data),
                    'error_handling': claude_docs.get('error_handling', self.helpers.get_error_handling(project_data)),
                    'module_tasks': self.formatters.format_module_tasks(module['name'], module_tasks.get(module['name'], [])),
                    'testing_strategy': self.helpers.get_testing_strategy(project_data),
                    'performance_notes': claude_docs.get('performance', 'To be defined based on requirements'),
                    'security_notes': claude_docs.get('security', 'To be defined based on requirements'),
                    'example_imports': 'specific_function, SpecificClass',
                    'usage_example': self.formatters.format_examples(claude_docs.get('examples', []))
                })
            else:
                module_context.update({
                    'module_name': module['name'],
                    'module_description': module['description'],
                    'module_responsibilities': self.helpers.get_module_responsibilities(module, project_data),
                    'public_api': 'To be defined during implementation',
                    'internal_architecture': 'To be defined during implementation',
                    'dependencies': self.helpers.get_module_dependencies(module, project_data),
                    'naming_conventions': self.helpers.get_naming_conventions(project_data),
                    'file_organization': self.helpers.get_file_organization(module, project_data),
                    'error_handling': self.helpers.get_error_handling(project_data),
                    'module_tasks': self.formatters.format_module_tasks(module['name'], module_tasks.get(module['name'], [])),
                    'testing_strategy': self.helpers.get_testing_strategy(project_data),
                    'performance_notes': 'To be defined based on requirements',
                    'security_notes': 'To be defined based on requirements',
                    'example_imports': 'specific_function, SpecificClass',
                    'usage_example': '# Actual usage examples will be added during implementation'
                })
            
            module_claude = self.templates.get_template('module_claude', module_context)
            (module_path / 'CLAUDE.md').write_text(module_claude)
            
            # Create module TODO.md
            module_todos = []
            if module['name'] in module_tasks:
                for task in module_tasks[module['name']]:
                    # Use Claude-enhanced subtasks if available
                    if 'details' in task and 'subtasks' in task['details']:
                        module_todos.append(f"\n## Task: {task['title']}")
                        for subtask in task['details']['subtasks']:
                            module_todos.append(f"- [ ] {subtask}")
                    else:
                        # Use default subtasks
                        module_todos.extend([
                            f"- [ ] Research: {task['title']}",
                            f"- [ ] Document findings for: {task['title']}",
                            f"- [ ] Write failing tests for: {task['title']}",
                            f"- [ ] Implement: {task['title']}",
                            f"- [ ] Verify all tests pass for: {task['title']}",
                            f"- [ ] Update documentation for: {task['title']}"
                        ])
            
            self.create_todo_file(
                module_path / 'TODO.md',
                module['name'],
                f"the {module['name']} module",
                module_todos
            )
            
            # Create research templates for tasks
            if module['name'] in module_tasks:
                for task in module_tasks[module['name']]:
                    research_file = module_path / 'docs' / f"{self.formatters.slugify(task['title'])}.md"
                    
                    # Use Claude-enhanced details if available
                    if 'details' in task:
                        details = task['details']
                        research_topics = details.get('research_topics', [])
                        research_questions = '\n'.join([f"- {topic}" for topic in research_topics]) if research_topics else '- What are the requirements?\n- What are the constraints?\n- What are the edge cases?\n- What patterns should we follow?'
                        
                        research_context = {
                            'task_name': task['title'],
                            'research_objective': details.get('goal', f"Research and document approach for: {task['title']}"),
                            'key_questions': research_questions,
                            'findings': 'To be completed during research phase',
                            'recommendations': 'To be completed during research phase',
                            'references': 'To be added during research',
                            'next_steps': '1. Complete research\n2. Write tests\n3. Implement solution'
                        }
                    else:
                        research_context = {
                            'task_name': task['title'],
                            'research_objective': f"Research and document approach for: {task['title']}",
                            'key_questions': '- What are the requirements?\n- What are the constraints?\n- What are the edge cases?\n- What patterns should we follow?',
                            'findings': 'To be completed during research phase',
                            'recommendations': 'To be completed during research phase',
                            'references': 'To be added during research',
                            'next_steps': '1. Complete research\n2. Write tests\n3. Implement solution'
                        }
                    
                    research_content = self.templates.workflow_templates['research_template'].format(**research_context)
                    research_file.write_text(research_content)
    
    def create_todo_file(self, file_path: Path, scope: str, scope_description: str, todo_items: List[str]):
        """Create a TODO.md file with enhanced formatting."""
        total = len(todo_items)
        completed = sum(1 for item in todo_items if '[x]' in item.lower())
        pending = total - completed
        completion_percentage = (completed / total * 100) if total > 0 else 0
        
        # Get recent completions (placeholder for now)
        recent_completions = "- No completed items yet"
        
        # Determine next steps
        next_steps = "1. Start with the first pending task\n2. Follow TDD methodology\n3. Update this file as you progress"
        
        context = {
            'scope': scope,
            'scope_description': scope_description,
            'status_summary': ff"{icons.CHART} {completed}/{total} tasks completed ({completion_percentage:.0f}%)",
            'todo_items': '\n'.join(todo_items) if todo_items else '- [ ] No tasks defined yet',
            'total_tasks': total,
            'completed_tasks': completed,
            'completion_percentage': completion_percentage,
            'in_progress_tasks': 0,
            'pending_tasks': pending,
            'recent_completions': recent_completions,
            'next_steps': next_steps,
            'timestamp': datetime.now().isoformat()
        }
        
        content = self.templates.get_template('todo_md', context)
        file_path.write_text(content)