"""Enhanced templates for Claude Scaffold projects."""

from datetime import datetime
from typing import Any, Dict

from ..utils.icons import icons
from .template_base import BaseTemplates
from .template_commands import CommandTemplates
from .template_project import ProjectSpecificTemplates
from .template_workflows import WorkflowTemplates


class ProjectTemplates:
    """Enhanced templates for Claude Scaffold projects."""

    def __init__(self):
        self.base_templates = BaseTemplates.get_templates()
        self.workflow_templates = WorkflowTemplates.get_templates()
        self.command_templates = CommandTemplates.get_templates()
        self.project_templates = ProjectSpecificTemplates.get_templates()

    def get_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Get a formatted template by name."""
        # Find the template
        template = None
        if template_name in self.base_templates:
            template = self.base_templates[template_name]
        elif template_name in self.workflow_templates:
            template = self.workflow_templates[template_name]
        elif template_name in self.command_templates:
            template = self.command_templates[template_name]
        elif template_name in self.project_templates:
            template = self.project_templates[template_name]
        else:
            raise ValueError(f"Template '{template_name}' not found")

        # Prepare and format context
        prepared_context = self._prepare_context(context)
        return template.format(**prepared_context)

    def _prepare_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare context for template formatting."""
        # Ensure all required fields have defaults
        defaults = {
            "timestamp": datetime.now().isoformat(),
            "project_structure": "Project structure will be generated",
            "module_overview": "Module overview will be generated",
            "tasks_by_module": "Tasks will be listed here",
            "todo_items": "- [ ] No tasks defined yet",
            "status_summary": f"{icons.CHART} 0/0 tasks completed (0%)",
            "recent_completions": "- No completed items yet",
            "next_steps": "1. Start with the first task",
            "example_imports": "example_function, ExampleClass",
            "usage_example": "# Usage examples will be added during implementation",
            "project_specific_ignores": "# Add project-specific patterns here",
            "commit_standards": "- Use conventional commits format\n- Clear, descriptive messages\n- Reference issue numbers when applicable",
            "icons": icons,  # Add icons object to context
        }

        # Merge with provided context
        prepared = defaults.copy()
        prepared.update(context)

        # Convert lists and dicts to formatted strings
        for key, value in prepared.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                prepared[key] = self._format_list_of_dicts(value)
            elif isinstance(value, dict) and key != "icons":  # Don't format the icons object
                prepared[key] = self._format_dict(value)

        return prepared

    def _format_list_of_dicts(self, items: list) -> str:
        """Format a list of dictionaries for display."""
        if not items:
            return "None"

        formatted = []
        for item in items:
            if "name" in item and "description" in item:
                formatted.append(f"- **{item['name']}**: {item['description']}")
            elif "title" in item and "module" in item:
                formatted.append(f"- [{item['module']}] {item['title']}")
            else:
                formatted.append(f"- {str(item)}")

        return "\n".join(formatted)

    def _format_dict(self, d: dict) -> str:
        """Format a dictionary for display."""
        if not d:
            return "None"

        formatted = []
        for key, value in d.items():
            if isinstance(value, list):
                formatted.append(f"**{key}**:")
                for item in value:
                    formatted.append(f"  - {item}")
            else:
                formatted.append(f"**{key}**: {value}")

        return "\n".join(formatted)

    def _indent(self, text: str, spaces: int = 2) -> str:
        """Indent text by specified spaces."""
        indent = " " * spaces
        return "\n".join(indent + line for line in text.split("\n"))
