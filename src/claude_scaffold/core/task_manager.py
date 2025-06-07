import sys
from pathlib import Path

from ..interactive.interactive_setup import InteractiveSetup
from ..templates.templates import ProjectTemplates
from ..utils.formatters import Formatters
from ..utils.icons import icons


class TaskManager:
    """Manages task operations for existing projects."""

    def __init__(self):
        self.interactive_setup = InteractiveSetup()
        self.templates = ProjectTemplates()
        self.formatters = Formatters()

    def add_task(
        self,
        project_path: Path,
        module_name: str,
        task_title: str,
        priority: str = "medium",
    ) -> bool:
        """Add a new task to an existing project."""
        # Load existing configuration
        config = self.interactive_setup.load_config(project_path)

        if not config:
            print(
                f"{icons.ERROR} Error: No Claude Scaffold configuration found at {project_path}",
                file=sys.stderr,
            )
            return False

        # Check if module exists
        module_exists = any(m["name"] == module_name for m in config["modules"])

        if not module_exists:
            print(
                f"{icons.ERROR} Error: Module '{module_name}' not found in project",
                file=sys.stderr,
            )
            print(f"   Available modules: {', '.join(m['name'] for m in config['modules'])}")
            return False

        # Add task to configuration
        new_task = {
            "title": task_title,
            "module": module_name,
            "priority": priority,
            "type": "added",
        }
        config["tasks"].append(new_task)

        # Update TASKS.md
        tasks_file = project_path / "TASKS.md"
        if tasks_file.exists():
            # Regenerate TASKS.md with new task
            from ..utils.project_helpers import ProjectHelpers

            helpers = ProjectHelpers()
            context = helpers.prepare_template_context(config)
            tasks_content = self.templates.get_template("tasks_md", context)
            tasks_file.write_text(tasks_content)

        # Update module CLAUDE.md
        module_path = project_path / module_name
        module_claude = module_path / "CLAUDE.md"

        if module_claude.exists():
            # Read existing content and add new task section
            content = module_claude.read_text()

            # Find the tasks section and add new task
            task_count = content.count("### Task ")
            new_task_section = f"\n### Task {task_count + 1} – {task_title}\n"
            new_task_section += f"**Priority**: {priority}\n"
            new_task_section += "**Goal**: To be defined during research phase\n"
            new_task_section += (
                f"**Research file**: docs/{self.formatters.slugify(task_title)}.md\n"
            )
            new_task_section += "**Sub-tasks**: see TODO.md\n"

            # Insert before the "## Testing Strategy" section or at the end of tasks
            lines = content.split("\n")
            insert_pos = None

            for i, line in enumerate(lines):
                if line.strip() == "## Testing Strategy":
                    insert_pos = i - 1
                    break

            if insert_pos:
                lines.insert(insert_pos, new_task_section)
                module_claude.write_text("\n".join(lines))
            else:
                module_claude.write_text(content + "\n" + new_task_section)

        # Update module TODO.md
        module_todo = module_path / "TODO.md"
        if module_todo.exists():
            content = module_todo.read_text()

            # Add new todo items
            new_todos = [
                f"- [ ] Research: {task_title}",
                f"- [ ] Document findings for: {task_title}",
                f"- [ ] Write failing tests for: {task_title}",
                f"- [ ] Implement: {task_title}",
                f"- [ ] Verify all tests pass for: {task_title}",
                f"- [ ] Update documentation for: {task_title}",
            ]

            # Find checklist section and add items
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.strip() == "## Checklist":
                    # Find the end of current checklist
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith("- [") or lines[j].strip() == ""):
                        j += 1

                    # Insert new todos
                    for todo in reversed(new_todos):
                        lines.insert(j, todo)

                    module_todo.write_text("\n".join(lines))
                    break

        # Create research template
        research_file = module_path / "docs" / f"{self.formatters.slugify(task_title)}.md"
        research_context = {
            "task_name": task_title,
            "research_objective": f"Research and document approach for: {task_title}",
            "key_questions": "- What are the requirements?\n- What are the constraints?\n- What are the edge cases?\n- What patterns should we follow?",
            "findings": "To be completed during research phase",
            "recommendations": "To be completed during research phase",
            "references": "To be added during research",
            "next_steps": "1. Complete research\n2. Write tests\n3. Implement solution",
        }
        research_content = self.templates.get_template(
            "research_template", research_context
        )
        research_file.write_text(research_content)

        # Save updated configuration
        self.interactive_setup.save_config(config, project_path)

        print(f"{icons.SUCCESS} Task '{task_title}' added to module '{module_name}'")
        print(
            f"{icons.DOCUMENT} Research template created at: {research_file.relative_to(project_path)}"
        )

        return True
