"""Interactive collectors for project information."""

import questionary
from typing import Dict, List, Any
import textwrap
from ..utils.icons import icons
from ..utils.ui_manager import ui_manager


class InteractiveCollectors:
    """Handles interactive collection of project information."""

    def __init__(self, project_config):
        self.project_config = project_config

    def collect_modules(self, project_data: Dict[str, Any]) -> List[Dict]:
        """Collect module information."""
        modules = []

        with ui_manager.live_status("Collecting Module Information") as status:
            suggested = self.project_config.project_types[
                project_data["metadata"]["project_type"]
            ]["suggested_modules"]

            # Ask about suggested modules
            if suggested:
                status.update(
                    "Processing suggested modules",
                    project_type=project_data["metadata"]["project_type_name"],
                    suggested_count=len(suggested),
                )

                print(
                    f"\n{icons.MODULE} Suggested modules for {project_data['metadata']['project_type_name']}:"
                )
                for module in suggested:
                    print(f"   {icons.BULLET} {module}")

                use_suggested = questionary.confirm(
                    "Would you like to use these suggested modules?", default=True
                ).ask()

                if use_suggested:
                    modules = [
                        {
                            "name": m,
                            "description": f"{m.title()} module",
                            "type": "suggested",
                        }
                        for m in suggested
                    ]
                    status.update(
                        f"Added {len(suggested)} suggested modules", progress=50
                    )

            # Allow adding custom modules
            custom_count = 0
            while True:
                add_more = questionary.confirm(
                    f"\n{'Add another module?' if modules else 'Add a module?'}",
                    default=len(modules) == 0,
                ).ask()

                if not add_more:
                    break

                status.update(f"Adding custom module {custom_count + 1}")

                module_name = questionary.text(
                    "Module name:",
                    validate=lambda x: len(x) > 0 and x.replace("_", "").isalnum(),
                ).ask()

                module_desc = questionary.text(
                    f"Description for {module_name} module:",
                    default=f"{module_name.title()} functionality",
                ).ask()

                modules.append(
                    {"name": module_name, "description": module_desc, "type": "custom"}
                )
                custom_count += 1

                status.update(
                    f"Added custom module: {module_name}",
                    custom_modules=custom_count,
                    total_modules=len(modules),
                )

            if not modules:
                modules = [
                    {
                        "name": "core",
                        "description": "Core functionality",
                        "type": "default",
                    }
                ]
                print(f"{icons.INFO} Added default 'core' module")

            status.success(f"Collected {len(modules)} modules")

        return modules

    def collect_tasks(
        self, project_data: Dict[str, Any], modules: List[Dict]
    ) -> List[Dict]:
        """Collect task information."""
        tasks = []

        with ui_manager.live_status("Collecting Task Information") as status:
            suggested_tasks = self.project_config.get_suggested_tasks(
                project_data["metadata"]["project_type"]
            )

            # Show suggested tasks
            if suggested_tasks:
                status.update(
                    "Processing suggested tasks",
                    project_type=project_data["metadata"]["project_type_name"],
                    suggested_count=len(suggested_tasks),
                )

                print(
                    f"\n{icons.TASK} Suggested tasks for {project_data['metadata']['project_type_name']}:"
                )
                for i, task in enumerate(suggested_tasks[:5], 1):
                    print(f"   {i}. {task}")
                if len(suggested_tasks) > 5:
                    print(f"   ... and {len(suggested_tasks) - 5} more")

                use_suggested = questionary.confirm(
                    "Would you like to select from these suggested tasks?", default=True
                ).ask()

                if use_suggested:
                    selected = questionary.checkbox(
                        "Select tasks to include:", choices=suggested_tasks
                    ).ask()

                    status.update(
                        f"Assigning {len(selected)} tasks to modules", progress=30
                    )

                    with ui_manager.step_progress(
                        f"Processing {len(selected)} selected tasks", len(selected)
                    ) as task_progress:
                        for i, task_title in enumerate(selected):
                            task_progress.update(
                                f"Configuring task: {task_title[:40]}..."
                            )

                            module = self._assign_task_to_module(task_title, modules)
                            priority = questionary.select(
                                f"Priority for '{task_title}':",
                                choices=["high", "medium", "low"],
                                default="medium",
                            ).ask()

                            tasks.append(
                                {
                                    "title": task_title,
                                    "module": module,
                                    "priority": priority,
                                    "type": "suggested",
                                }
                            )

                        task_progress.complete(f"Configured {len(selected)} tasks")

            # Allow adding custom tasks
            custom_count = 0
            while True:
                add_more = questionary.confirm(
                    f"\n{'Add another task?' if tasks else 'Add a task?'}",
                    default=len(tasks) < 3,
                ).ask()

                if not add_more:
                    break

                status.update(f"Adding custom task {custom_count + 1}")

                task_title = questionary.text(
                    "Task title:", validate=lambda x: len(x) > 0
                ).ask()

                module = questionary.select(
                    f"Which module should handle '{task_title}'?",
                    choices=[m["name"] for m in modules],
                ).ask()

                priority = questionary.select(
                    "Task priority:",
                    choices=["high", "medium", "low"],
                    default="medium",
                ).ask()

                tasks.append(
                    {
                        "title": task_title,
                        "module": module,
                        "priority": priority,
                        "type": "custom",
                    }
                )
                custom_count += 1

                status.update(
                    f"Added custom task: {task_title[:40]}",
                    custom_tasks=custom_count,
                    total_tasks=len(tasks),
                )

            status.success(f"Collected {len(tasks)} tasks")

        return tasks

    def collect_rules(self, project_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Collect project rules."""
        rules = {"suggested": [], "custom": []}

        # Get suggested rules
        suggested = self.project_config.project_types[
            project_data["metadata"]["project_type"]
        ]["suggested_rules"]

        if suggested:
            print(
                f"\n{icons.RULE} Suggested rules for {project_data['metadata']['project_type_name']}:"
            )
            for rule in suggested:
                print(f"   {icons.BULLET} {rule}")

            from questionary import Choice

            rule_choices = [Choice(rule, checked=True) for rule in suggested]

            selected = questionary.checkbox(
                "Select rules to include:", choices=rule_choices
            ).ask()

            rules["suggested"] = selected

        # Common rules
        common_rules = [
            "Write tests before implementation (TDD)",
            "All tests must pass before merging",
            "Document all public APIs",
            "No hardcoded credentials",
            "Handle errors gracefully",
            "Follow semantic versioning",
            "Code reviews required for all changes",
        ]

        print("\n{icons.RULE} Common project rules:")
        for rule in common_rules[:5]:
            print(f"   {icons.BULLET} {rule}")

        selected_common = questionary.checkbox(
            "Select additional rules:", choices=common_rules
        ).ask()

        rules["suggested"].extend(selected_common)

        # Custom rules
        while questionary.confirm("\nAdd a custom rule?", default=False).ask():
            custom_rule = questionary.text(
                "Enter custom rule:", validate=lambda x: len(x) > 0
            ).ask()
            rules["custom"].append(custom_rule)

        return rules

    def collect_additional_config(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect additional configuration."""
        # Technical constraints
        print(f"\n{icons.CONFIG} Technical Constraints")
        constraints = []

        # Language version
        if project_data["metadata"]["language"] in ["Python", "Both"]:
            py_version = questionary.text(
                "Minimum Python version:", default="3.8+"
            ).ask()
            constraints.append(f"Python {py_version}")

        # Add custom constraints
        while questionary.confirm("Add another constraint?", default=False).ask():
            constraint = questionary.text("Enter constraint:").ask()
            if constraint:
                constraints.append(constraint)

        project_data["constraints"] = constraints

        # Build commands
        print("\n{icons.BUILD} Build & Development Commands")
        default_commands = self.project_config.project_types[
            project_data["metadata"]["project_type"]
        ]["build_commands"]

        commands = {}
        command_types = ["install", "test", "build", "dev", "lint"]

        for cmd_type in command_types:
            default = next(
                (cmd for cmd in default_commands if cmd_type in cmd.lower()), ""
            )
            command = questionary.text(
                f"{cmd_type.title()} command:", default=default
            ).ask()
            if command:
                commands[cmd_type] = command

        project_data["metadata"]["commands"] = commands

        # Git configuration
        print(f"\n{icons.REFRESH} Version Control")
        git_init = questionary.confirm("Initialize git repository?", default=True).ask()

        if git_init:
            initial_branch = questionary.text(
                "Initial branch name:", default="main"
            ).ask()

            project_data["metadata"]["git"] = {
                "init": True,
                "initial_branch": initial_branch,
            }

        return project_data

    def _assign_task_to_module(self, task_title: str, modules: List[Dict]) -> str:
        """Intelligently assign a task to a module based on keywords."""
        task_lower = task_title.lower()

        # Keyword mapping
        keyword_map = {
            "auth": ["auth", "login", "user", "permission", "security"],
            "api": ["api", "endpoint", "route", "rest", "graphql"],
            "database": ["database", "schema", "model", "migration", "query"],
            "frontend": ["ui", "component", "view", "frontend", "interface"],
            "backend": ["backend", "server", "service", "logic"],
            "data": ["data", "dataset", "preprocessing", "pipeline"],
            "models": ["model", "training", "prediction", "ml", "ai"],
            "utils": ["utility", "helper", "tool", "format", "logging"],
            "config": ["config", "setting", "environment", "setup"],
            "commands": ["command", "cli", "argument", "parse"],
        }

        # Try to find a matching module
        for module in modules:
            module_name = module["name"].lower()

            # Direct match
            if module_name in task_lower:
                return module["name"]

            # Keyword match
            if module_name in keyword_map:
                for keyword in keyword_map[module_name]:
                    if keyword in task_lower:
                        return module["name"]

        # Ask user if no match found
        return questionary.select(
            f"Which module should handle '{task_title}'?",
            choices=[m["name"] for m in modules],
        ).ask()
