from datetime import datetime
from typing import Dict, Any

from .formatters import Formatters
from .icons import Icons


class ProjectHelpers:
    """Helper methods for project configuration and setup."""
    
    def __init__(self):
        self.formatters = Formatters()
    
    def get_default_project_data(self, project_name: str) -> Dict[str, Any]:
        """Get minimal default project data for non-interactive mode."""
        return {
            'project_name': project_name,
            'timestamp': datetime.now().isoformat(),
            'version': '0.1.0',
            'modules': [
                {'name': 'core', 'description': 'Core functionality', 'type': 'default'}
            ],
            'tasks': [],
            'rules': {
                'suggested': ['Follow PEP 8 style guide', 'Write comprehensive tests'],
                'custom': []
            },
            'constraints': ['Python 3.8+'],
            'metadata': {
                'project_type': 'custom',
                'project_type_name': 'Custom Project',
                'description': f'{project_name} - A Claude Scaffold project',
                'language': 'Python',
                'style_guide': 'pep8',
                'test_framework': 'pytest',
                'commands': {
                    'install': 'pip install -e .',
                    'test': 'pytest',
                    'lint': 'flake8 .'
                }
            }
        }
    
    def prepare_template_context(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare comprehensive context for templates."""
        metadata = project_data.get('metadata', {})
        
        # Count tasks by priority
        high_priority = sum(1 for t in project_data['tasks'] if t.get('priority') == 'high')
        medium_priority = sum(1 for t in project_data['tasks'] if t.get('priority') == 'medium')
        low_priority = sum(1 for t in project_data['tasks'] if t.get('priority') == 'low')
        
        # Format commands
        commands = metadata.get('commands', {})
        build_commands = []
        for cmd_type, cmd in commands.items():
            if cmd:
                build_commands.append(f"- **{cmd_type}**: `{cmd}`")
        
        # Format module overview
        module_overview = []
        for module in project_data['modules']:
            module_overview.append(f"### {module['name']}")
            module_overview.append(f"{module['description']}")
            module_overview.append("")
        
        style_guides = {
            'pep8': 'PEP 8 Style Guide',
            'black': 'Black Code Formatter',
            'google': 'Google Python Style Guide',
            'custom': 'Custom style guide'
        }
        
        context = {
            'project_name': project_data['project_name'],
            'description': metadata.get('description', 'A Claude Scaffold project'),
            'version': project_data.get('version', '0.1.0'),
            'timestamp': project_data.get('timestamp', datetime.now().isoformat()),
            'project_type': metadata.get('project_type_name', 'Custom'),
            'language': metadata.get('language', 'Python'),
            'style_guide': style_guides.get(
                metadata.get('style_guide', 'custom'),
                'Custom style guide'
            ),
            'install_command': commands.get('install', 'pip install -e .'),
            'test_command': commands.get('test', 'pytest'),
            'dev_command': commands.get('dev', 'python main.py'),
            'project_structure': 'Will be generated after creation',
            'style_conventions': self.get_style_conventions(project_data),
            'architecture_patterns': self.get_architecture_patterns(project_data),
            'module_overview': '\n'.join(module_overview),
            'build_commands': '\n'.join(build_commands) if build_commands else 'No build commands configured',
            'code_quality_rules': self.get_code_quality_rules(project_data),
            'architecture_rules': self.get_architecture_rules(project_data),
            'testing_rules': self.get_testing_rules(project_data),
            'documentation_rules': self.get_documentation_rules(project_data),
            'git_workflow': self.get_git_workflow(project_data),
            'project_rules': self.formatters.format_project_rules(project_data),
            'constraints': self.formatters.format_constraints(project_data),
            'commit_standards': self.get_commit_standards(project_data),
            'total_tasks': len(project_data['tasks']),
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': low_priority,
            'tasks_by_module': self.formatters.format_tasks_by_module(project_data),
            'modules': project_data['modules'],
            'tasks': project_data['tasks'],
            'icons': Icons  # Add Icons class to context
        }
        
        return context
    
    def get_module_responsibilities(self, module: Dict, project_data: Dict) -> str:
        """Get module responsibilities based on type and name."""
        # Add intelligent responsibility assignment based on module name
        return f"- Primary responsibility for {module['description']}\n- Maintain clean interfaces with other modules\n- Ensure comprehensive test coverage"
    
    def get_module_dependencies(self, module: Dict, project_data: Dict) -> str:
        """Get module dependencies."""
        # This could be enhanced to analyze module relationships
        return "- Standard library modules\n- Project core utilities\n- External dependencies as defined in requirements"
    
    def get_naming_conventions(self, project_data: Dict) -> str:
        """Get naming conventions based on style guide."""
        style = project_data['metadata'].get('style_guide', 'pep8')
        
        if style in ['pep8', 'google', 'black']:
            return """- Classes: PascalCase (e.g., `AudioProcessor`)
- Functions/methods: snake_case (e.g., `process_audio`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_BUFFER_SIZE`)
- Private methods: leading underscore (e.g., `_internal_method`)
- Module files: snake_case (e.g., `audio_utils.py`)"""
        else:
            return "- Follow project-specific naming conventions as defined in GLOBAL_RULES.md"
    
    def get_file_organization(self, module: Dict, project_data: Dict) -> str:
        """Get file organization guidelines."""
        return """- Group related functionality in single files
- Keep files focused and under 500 lines
- Use __init__.py to expose public API
- Place internal utilities in _utils.py or similar"""
    
    def get_error_handling(self, project_data: Dict) -> str:
        """Get error handling guidelines."""
        return """- Use specific exception types
- Provide helpful error messages
- Log errors appropriately
- Never silently swallow exceptions
- Document expected exceptions in docstrings"""
    
    def get_testing_strategy(self, project_data: Dict) -> str:
        """Get testing strategy based on project type."""
        test_framework = project_data['metadata'].get('test_framework', 'pytest')
        
        return f"""- Test framework: {test_framework}
- Minimum coverage target: 80%
- Write tests before implementation (TDD)
- Include unit and integration tests
- Test edge cases and error conditions
- Use mocks for external dependencies"""
    
    def get_style_conventions(self, project_data: Dict) -> str:
        """Get style conventions based on style guide."""
        style = project_data['metadata'].get('style_guide', 'pep8')
        conventions = []
        
        if style == 'pep8':
            conventions.extend([
                "- Follow PEP 8 strictly",
                "- Maximum line length: 79 characters",
                "- Use 4 spaces for indentation"
            ])
        elif style == 'black':
            conventions.extend([
                "- Use Black formatter (line length: 88)",
                "- Run `black .` before committing",
                "- No manual formatting"
            ])
        
        # Add language-specific conventions
        if project_data['metadata'].get('language') in ['Python', 'Both']:
            conventions.extend([
                "- Use type hints for all public functions",
                "- Docstrings for all public modules, classes, and functions"
            ])
        
        return '\n'.join(conventions)
    
    def get_architecture_patterns(self, project_data: Dict) -> str:
        """Get architecture patterns based on project type."""
        project_type = project_data['metadata'].get('project_type')
        
        patterns = {
            'web': "- MVC/MVP pattern for web components\n- RESTful API design\n- Separation of concerns",
            'cli': "- Command pattern for CLI actions\n- Strategy pattern for output formats\n- Clear separation of UI and logic",
            'library': "- Clean public API\n- Minimal dependencies\n- Extensible design patterns",
            'api': "- Repository pattern for data access\n- Service layer for business logic\n- DTO pattern for data transfer",
            'ml': "- Pipeline pattern for data processing\n- Strategy pattern for models\n- Observer pattern for metrics"
        }
        
        return patterns.get(project_type, "- Follow SOLID principles\n- Maintain loose coupling\n- Prefer composition over inheritance")
    
    def get_code_quality_rules(self, project_data: Dict) -> str:
        """Get code quality rules."""
        rules = ["- All code must pass linting checks", "- No commented-out code in commits"]
        
        if project_data['metadata'].get('language') in ['Python', 'Both']:
            rules.extend([
                "- Type hints required for public APIs",
                "- Docstrings required for public modules/classes/functions",
                "- No mutable default arguments"
            ])
        
        return '\n'.join(rules)
    
    def get_architecture_rules(self, project_data: Dict) -> str:
        """Get architecture rules."""
        return """- Follow established patterns consistently
- No circular dependencies between modules
- Keep coupling loose and cohesion high
- Document architectural decisions in ADRs (Architecture Decision Records)"""
    
    def get_testing_rules(self, project_data: Dict) -> str:
        """Get testing rules."""
        return """- Write tests BEFORE implementation (TDD)
- Tests must actually fail before implementation
- Maintain minimum 80% code coverage
- Include both positive and negative test cases
- Mock external dependencies
- Tests must be deterministic and fast"""
    
    def get_documentation_rules(self, project_data: Dict) -> str:
        """Get documentation rules."""
        return """- Keep documentation close to code
- Update docs with code changes
- Include examples in documentation
- Document "why" not just "what"
- Use clear, concise language
- Maintain README.md and CLAUDE.md files"""
    
    def get_git_workflow(self, project_data: Dict) -> str:
        """Get git workflow guidelines."""
        return """- Commit early and often
- Write descriptive commit messages
- Use conventional commits format
- Never commit sensitive data
- Keep commits focused and atomic
- Squash commits before merging if needed"""
    
    def get_commit_standards(self, project_data: Dict) -> str:
        """Get commit message standards."""
        return """Format: `<type>(<scope>): <subject>`

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test additions/changes
- chore: Build/tooling changes

Example: `feat(auth): add user login functionality`"""
    
    def get_project_specific_ignores(self, project_data: Dict) -> str:
        """Get project-specific gitignore entries."""
        ignores = []
        
        project_type = project_data['metadata'].get('project_type')
        
        if project_type == 'web':
            ignores.extend(['node_modules/', 'dist/', 'build/', '*.min.js', '*.min.css'])
        elif project_type == 'ml':
            ignores.extend(['data/raw/', 'models/*.pkl', 'models/*.h5', '*.ipynb_checkpoints'])
        elif project_type == 'api':
            ignores.extend(['*.db', 'migrations/versions/', 'instance/'])
        
        return '\n'.join(ignores)