"""Base templates for Claude Scaffold projects."""

from typing import Dict


class BaseTemplates:
    """Base templates used across all project types."""

    @staticmethod
    def get_templates() -> Dict[str, str]:
        """Return all base templates."""
        return {
            "root_claude": """# {project_name} Claude Documentation

## 🚨 IMPORTANT: System Instructions for Claude

**CRITICAL**: When working on this project, you MUST:

1. **ONLY implement the modules listed in the "Modules" section below**
   - Do NOT create additional modules beyond what is specified
   - Do NOT add features or functionality outside the defined scope

2. **ONLY work on tasks listed in TASKS.md**
   - Each task has been carefully planned and scoped
   - Task details are in the respective module's CLAUDE.md file
   - Do NOT add tasks or features not explicitly listed

3. **Follow the exact project structure as defined**
   - Respect the module boundaries and responsibilities
   - Maintain the architectural decisions made during setup
   - Do NOT reorganize or restructure without explicit instruction

4. **Adhere to all rules in GLOBAL_RULES.md**
   - These rules are immutable and override any other conventions
   - When in doubt, refer to GLOBAL_RULES.md

This project has been scaffolded according to specific requirements. Your role is to implement ONLY what has been defined, not to extend or modify the scope."""
            + """

---

## Overview
{description}

**Project Type**: {project_type}
**Primary Language**: {language}
**Style Guide**: {style_guide}

## Quick Start

```bash
# Install dependencies
{install_command}

# Run tests
{test_command}

# Start development
{dev_command}
```

## Project Structure
```
{project_structure}
```

## Modules

{module_overview}

## Development Workflow

1. **Research First**: Before implementing any feature, research and document your approach """
            + """in the relevant `docs/` folder
2. **Test-Driven Development**: Write failing tests before implementation
3. **Implement**: Write the minimum code to make tests pass
4. **Refactor**: Clean up while keeping tests green
5. **Document**: Update relevant documentation

## Style Conventions
{style_conventions}

## Architecture Patterns
{architecture_patterns}

## Build Commands
{build_commands}

## Team Conventions

### Code Reviews
- All code must be reviewed before merging
- Use pull request templates
- Check tests pass and coverage maintained

### Documentation
- Keep docs in sync with code
- Document "why" not just "what"
- Include examples where helpful

Generated on: {timestamp}
""",
            "global_rules": """# Global Rules for {project_name}

These rules are **immutable** and must be followed throughout the project lifecycle.

## 0. FUNDAMENTAL PROJECT SCOPE RULE

{icons.ERROR} **ABSOLUTE REQUIREMENT**: This project's scope is FIXED at creation time:

- **Modules**: ONLY the modules defined in CLAUDE.md are allowed
- **Tasks**: ONLY the tasks listed in TASKS.md should be implemented
- **Features**: NO additional features beyond what's explicitly specified
- **Structure**: NO restructuring or reorganization without explicit instruction

The project was scaffolded based on specific requirements. Your role is to implement what has been defined, not to extend the scope.

## 1. Code Quality Rules
{code_quality_rules}

## 2. Architecture Rules
{architecture_rules}

## 3. Testing Rules
{testing_rules}

## 4. Documentation Rules
{documentation_rules}

## 5. Git Workflow
{git_workflow}

## 6. Project-Specific Rules
{project_rules}

## 7. Technical Constraints
{constraints}

## Commit Message Standards
{commit_standards}

---
{icons.WARNING} **IMPORTANT**: These rules override any conflicting conventions. When in doubt, refer to this document.

Generated on: {timestamp}
""",
            "tasks_md": """# Task List for {project_name}

**Total Tasks**: {total_tasks} ({high_priority} high, {medium_priority} medium, {low_priority} low)

## Overview
This file contains a complete list of all tasks. Detailed specifications for each task can be found in the respective module's CLAUDE.md file.

## Tasks by Module
{tasks_by_module}

## Task Management Workflow

1. **Select a task** from the list above
2. **Navigate** to the module's CLAUDE.md for detailed specifications
3. **Research** using the docs/[task_name].md template
4. **Follow TDD** as tracked in the module's TODO.md
5. **Update progress** by checking off items in TODO.md

## Priority Legend
- {icons.ERROR} High Priority - Critical path or blocking other work
- {icons.WARNING} Medium Priority - Important but not blocking
- {icons.SUCCESS} Low Priority - Nice to have or can be deferred

Generated on: {timestamp}
""",
            "todo_md": """# TODO List for {scope}

**Scope**: Tasks and progress for {scope_description}
**Status**: {status_summary}
**Last Updated**: {timestamp}

## Checklist

{todo_items}

## Progress Summary

- **Total Tasks**: {total_tasks}
- **Completed**: {completed_tasks} {icons.SUCCESS}
- **In Progress**: {in_progress_tasks} 🚧
- **Pending**: {pending_tasks} ⏳
- **Completion**: {completion_percentage:.0f}%

## Recent Completions
{recent_completions}

## Next Steps
{next_steps}

---
{icons.INFO} **Tip**: Update this file as you complete tasks. Use `[x]` to mark completed items.
""",
            "module_claude": """# {module_name} Module Documentation

## {icons.ERROR} MODULE SCOPE REMINDER

This module's scope is FIXED. You must:
- ONLY implement the tasks listed in the "Tasks" section below
- NOT add new features or functionality beyond what's specified
- MAINTAIN the defined responsibilities and boundaries
- FOLLOW the architecture patterns established for this module

## Overview
{module_description}

## Responsibilities
{module_responsibilities}

## Public API
{public_api}

## Internal Architecture
{internal_architecture}

## Dependencies
{dependencies}

## Module Conventions

### Naming Conventions
{naming_conventions}

### File Organization
{file_organization}

### Error Handling
{error_handling}

## Tasks

{module_tasks}

## Testing Strategy
{testing_strategy}

## Performance Considerations
{performance_notes}

## Security Considerations
{security_notes}

## Integration Points

### Imports from this module
```python
from {module_name} import {example_imports}
from ..utils.icons import icons
```

### Example Usage
```python
{usage_example}
```

## Change Log
- {timestamp}: Module created

---
{icons.DOCUMENT} **Note**: Keep this documentation updated as the module evolves.
""",
        }
