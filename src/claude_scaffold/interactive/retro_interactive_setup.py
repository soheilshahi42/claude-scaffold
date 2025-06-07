"""Retro-themed interactive setup with full-screen UI."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import time

from ..claude.claude_interactive_enhanced import EnhancedClaudeInteractiveSetup
from ..config.project_config import ProjectConfig
from ..utils.icons import icons
from ..utils.retro_ui import RetroUI


class RetroInteractiveSetup:
    """Interactive setup with retro full-screen UI."""
    
    def __init__(self, use_claude: bool = True, debug_mode: bool = False):
        self.ui = RetroUI()
        self.project_config = ProjectConfig()
        self.use_claude = use_claude
        self.debug_mode = debug_mode
        
        # Use Claude-enhanced setup if available
        if use_claude:
            self.claude_setup = EnhancedClaudeInteractiveSetup(debug_mode)
        else:
            self.claude_setup = None
    
    def _refine_with_retro_ui(
        self,
        current_value: Any,
        title: str,
        subtitle: str = "",
        value_type: str = "text",
        max_iterations: int = 3
    ) -> Any:
        """Allow user to iteratively refine Claude's suggestion with feedback."""
        refined_value = current_value
        iteration = 0
        
        while iteration < max_iterations:
            # Ask if they want to refine
            feedback = self.ui.ask_feedback(
                title,
                refined_value,
                value_type,
                f"{subtitle} - Iteration {iteration + 1}/{max_iterations}"
            )
            
            if not feedback:
                # No feedback means accept as is
                return refined_value
            
            # Show progress while Claude processes feedback
            self.ui.show_progress(
                "REFINING SUGGESTION",
                "Claude is processing your feedback...",
                "AI refinement in progress"
            )
            
            try:
                # Build refinement prompt based on type
                if value_type == "text":
                    prompt = f"""Refine this text based on user feedback:

Current version: {refined_value}

User feedback: {feedback}

Provide an improved version based on the feedback. Return only the improved text."""
                elif value_type == "list":
                    import json
                    prompt = f"""Refine this list based on user feedback:

Current items: {json.dumps(refined_value)}

User feedback: {feedback}

Provide an improved list based on the feedback. Return a JSON array."""
                
                # Get refined result from Claude
                response = self.claude_setup.processor._call_claude(
                    prompt, 
                    expect_json=(value_type != "text")
                )
                
                if value_type == "text":
                    refined_value = response.strip()
                else:
                    import json
                    refined_value = json.loads(response)
                
                self.ui.stop_progress()
                
                # Show refined result
                self.ui.show_results(
                    "REFINED RESULT",
                    {"Result": refined_value},
                    "Claude has updated the suggestion"
                )
                
                # Ask if they want to continue refining
                continue_refining = self.ui.ask_confirm(
                    "CONTINUE REFINEMENT",
                    "Would you like to refine further?",
                    default=False,
                    subtitle=f"Iteration {iteration + 1} complete"
                )
                
                if not continue_refining:
                    return refined_value
                    
                iteration += 1
                
            except Exception as e:
                self.ui.stop_progress()
                self.ui.show_results(
                    "REFINEMENT ERROR",
                    {"Error": str(e)},
                    "Failed to process refinement"
                )
                return refined_value
        
        return refined_value
            
    def run(self, project_name: str) -> Dict[str, Any]:
        """Run the retro interactive setup."""
        try:
            # Show welcome screen
            self.ui.show_welcome_screen(project_name)
            
            # Initialize project data
            project_data = {
                "project_name": project_name,
                "timestamp": datetime.now().isoformat(),
                "version": "0.1.0",
                "enhanced_with_claude": self.use_claude,
                "metadata": {},
            }
            
            # Run setup steps
            project_data = self._collect_project_type(project_data)
            project_data = self._collect_description(project_data)
            project_data = self._collect_language(project_data)
            project_data = self._collect_modules(project_data)
            project_data = self._collect_tasks(project_data)
            project_data = self._collect_rules(project_data)
            project_data = self._collect_additional_config(project_data)
            
            # Show final review
            if not self._review_and_confirm(project_data):
                raise KeyboardInterrupt("Setup cancelled by user")
                
            # Show completion
            self.ui.show_completion(
                "PROJECT CONFIGURED",
                f"Project '{project_name}' is ready!",
                {
                    "Modules": len(project_data.get("modules", [])),
                    "Tasks": len(project_data.get("tasks", [])),
                    "Rules": len(project_data.get("rules", {}).get("suggested", [])),
                },
                "Setup Complete"
            )
            
            return project_data
            
        except KeyboardInterrupt:
            self.ui.show_completion(
                "SETUP CANCELLED",
                "Project setup was cancelled",
                None,
                "Cancelled"
            )
            raise
            
    def _collect_project_type(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect project type with retro UI."""
        project_types = []
        for key, value in self.project_config.project_types.items():
            project_types.append({
                "name": f"{value['name']} - {value['description']}",
                "value": key
            })
            
        project_type = self.ui.ask_selection(
            "PROJECT TYPE",
            "Select your project type:",
            project_types,
            "Step 1 of 7",
            "Choose the type that best fits your project"
        )
        
        project_data["metadata"]["project_type"] = project_type
        project_data["metadata"]["project_type_name"] = self.project_config.project_types[
            project_type
        ]["name"]
        
        return project_data
        
    def _collect_description(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect project description with retro UI."""
        # Show progress while Claude thinks (if enabled)
        if self.use_claude:
            self.ui.show_progress(
                "AI ENHANCEMENT",
                "Claude is analyzing your project type...",
                "Preparing intelligent suggestions",
                [
                    "Understanding project requirements",
                    "Generating contextual suggestions",
                    "Optimizing configuration"
                ]
            )
            time.sleep(1)  # Give time to see the animation
            self.ui.stop_progress()
            
        description = self.ui.ask_text(
            "PROJECT DESCRIPTION",
            "Brief project description:",
            default=f"A {project_data['metadata']['project_type_name'].lower()} built with Claude Scaffold",
            subtitle="Step 2 of 7",
            hint="Describe what your project will do"
        )
        
        project_data["metadata"]["description"] = description
        
        # Claude enhancement
        if self.use_claude and self.claude_setup:
            self.ui.show_progress(
                "ENHANCING DESCRIPTION",
                "Claude is enhancing your description...",
                "AI-powered optimization"
            )
            
            # Get enhanced description
            enhanced_desc = self.claude_setup._enhance_description(project_data)
            self.ui.stop_progress()
            
            if enhanced_desc and enhanced_desc != description:
                # Show Claude's suggestion
                use_enhanced = self.ui.ask_confirm(
                    "CLAUDE SUGGESTION",
                    f"Use Claude's enhanced description?\n\n{enhanced_desc}",
                    default=True,
                    subtitle="AI Enhancement",
                    hint="Claude has improved your description"
                )
                
                if use_enhanced:
                    # Allow iterative refinement
                    refined_desc = self._refine_with_retro_ui(
                        enhanced_desc,
                        "REFINE DESCRIPTION",
                        "AI-powered refinement",
                        value_type="text",
                        max_iterations=3
                    )
                    project_data["metadata"]["description"] = refined_desc
                    
        return project_data
        
    def _collect_language(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect programming language with retro UI."""
        languages = ["Python", "JavaScript", "TypeScript", "Both", "Other"]
        
        # Smart default based on description
        if (
            "react" in project_data["metadata"]["description"].lower()
            and "django" in project_data["metadata"]["description"].lower()
        ):
            default_idx = languages.index("Both")
        else:
            default_idx = 0
            
        language = self.ui.ask_selection(
            "PROGRAMMING LANGUAGE",
            "Primary programming language:",
            languages,
            "Step 3 of 7",
            "Select the main language for your project"
        )
        
        project_data["metadata"]["language"] = language
        return project_data
        
    def _collect_modules(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect modules with retro UI."""
        modules = []
        
        if self.use_claude and self.claude_setup:
            # Get Claude's suggestions
            self.ui.show_progress(
                "MODULE GENERATION",
                "Claude is designing your module structure...",
                "AI-powered architecture",
                [
                    "Analyzing project requirements",
                    "Designing module boundaries",
                    "Optimizing code organization"
                ]
            )
            
            claude_modules = self.claude_setup._get_claude_module_suggestions(project_data)
            self.ui.stop_progress()
            
            if claude_modules:
                # Show suggestions
                module_list = "\n".join([f"• {m}" for m in claude_modules[:10]])
                use_suggested = self.ui.ask_confirm(
                    "CLAUDE MODULES",
                    f"Use Claude's suggested modules?\n\n{module_list}",
                    default=True,
                    subtitle="AI Architecture",
                    hint=f"Claude suggests {len(claude_modules)} modules"
                )
                
                if use_suggested:
                    # Generate descriptions
                    self.ui.show_progress(
                        "GENERATING DESCRIPTIONS",
                        "Creating module descriptions...",
                        "AI-powered documentation"
                    )
                    
                    modules = [
                        {"name": m, "description": f"{m.title()} module"}
                        for m in claude_modules
                    ]
                    
                    # Get descriptions from Claude
                    if hasattr(self.claude_setup, 'processor'):
                        module_names = [m["name"] for m in modules]
                        descriptions = self.claude_setup.processor.generate_module_descriptions_batch(
                            module_names, project_data
                        )
                        
                        for module in modules:
                            if module["name"] in descriptions:
                                module["description"] = descriptions[module["name"]]
                                
                    self.ui.stop_progress()
                    
                    # Allow refinement of modules
                    want_refine = self.ui.ask_confirm(
                        "REFINE MODULES",
                        "Would you like to refine the module list?",
                        default=False,
                        subtitle="Claude has generated module descriptions"
                    )
                    
                    if want_refine:
                        modules = self._refine_with_retro_ui(
                            modules,
                            "REFINE MODULES",
                            "Module refinement",
                            value_type="list",
                            max_iterations=3
                        )
                                
        else:
            # Use default suggestions
            suggested = self.project_config.project_types[
                project_data["metadata"]["project_type"]
            ]["suggested_modules"]
            
            if suggested:
                module_list = "\n".join([f"• {m}" for m in suggested])
                use_suggested = self.ui.ask_confirm(
                    "SUGGESTED MODULES",
                    f"Use these suggested modules?\n\n{module_list}",
                    default=True,
                    subtitle="Step 4 of 7"
                )
                
                if use_suggested:
                    modules = [{"name": m, "description": f"{m.title()} module"} for m in suggested]
                    
        # Allow adding custom modules
        while True:
            add_more = self.ui.ask_confirm(
                "ADD MODULE",
                f"{'Add another module?' if modules else 'Add a module?'}",
                default=len(modules) == 0,
                subtitle=f"Currently have {len(modules)} modules"
            )
            
            if not add_more:
                break
                
            module_name = self.ui.ask_text(
                "MODULE NAME",
                "Module name:",
                subtitle=f"Module {len(modules) + 1}",
                hint="Use lowercase with underscores (e.g., user_auth)"
            )
            
            if module_name:
                module_desc = self.ui.ask_text(
                    "MODULE DESCRIPTION",
                    f"Description for {module_name}:",
                    default=f"{module_name.title()} functionality",
                    subtitle=f"Describing {module_name}"
                )
                
                modules.append({"name": module_name, "description": module_desc})
                
        project_data["modules"] = modules
        return project_data
        
    def _collect_tasks(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect tasks with retro UI."""
        tasks = []
        
        if self.use_claude and self.claude_setup:
            # Get Claude's suggestions
            self.ui.show_progress(
                "TASK GENERATION",
                "Claude is creating your task list...",
                "AI-powered planning",
                [
                    "Analyzing modules",
                    "Breaking down requirements",
                    "Prioritizing work items"
                ]
            )
            
            suggested_tasks = self.claude_setup._get_claude_task_suggestions(project_data)
            self.ui.stop_progress()
            
            if suggested_tasks:
                # Show task summary
                task_summary = f"Claude suggests {len(suggested_tasks)} tasks:\n\n"
                for i, task in enumerate(suggested_tasks[:5], 1):
                    priority_icon = icons.get_priority_icon(task.get("priority", "medium"))
                    task_summary += f"{priority_icon} [{task['module']}] {task['title']}\n"
                if len(suggested_tasks) > 5:
                    task_summary += f"\n...and {len(suggested_tasks) - 5} more tasks"
                    
                use_suggested = self.ui.ask_confirm(
                    "CLAUDE TASKS",
                    task_summary,
                    default=True,
                    subtitle="AI Task Planning",
                    hint="Review and accept Claude's task list"
                )
                
                if use_suggested:
                    # For simplicity, take first 10-15 tasks
                    tasks = suggested_tasks[:15]
                    
                    # Allow refinement of tasks
                    want_refine = self.ui.ask_confirm(
                        "REFINE TASKS",
                        "Would you like to refine the task list?",
                        default=False,
                        subtitle="Claude has generated tasks"
                    )
                    
                    if want_refine:
                        tasks = self._refine_with_retro_ui(
                            tasks,
                            "REFINE TASKS",
                            "Task refinement",
                            value_type="list",
                            max_iterations=3
                        )
                    
        # Allow adding custom tasks
        while self.ui.ask_confirm(
            "ADD TASK",
            f"{'Add another task?' if tasks else 'Add a task?'}",
            default=len(tasks) < 3,
            subtitle=f"Currently have {len(tasks)} tasks"
        ):
            task_title = self.ui.ask_text(
                "TASK TITLE",
                "Task title:",
                subtitle=f"Task {len(tasks) + 1}"
            )
            
            if task_title and project_data.get("modules"):
                module = self.ui.ask_selection(
                    "TASK MODULE",
                    f"Which module should handle '{task_title}'?",
                    [m["name"] for m in project_data["modules"]],
                    subtitle="Assign to module"
                )
                
                priority = self.ui.ask_selection(
                    "TASK PRIORITY",
                    "Task priority:",
                    ["high", "medium", "low"],
                    subtitle="Set priority level"
                )
                
                tasks.append({
                    "title": task_title,
                    "module": module,
                    "priority": priority
                })
                
        project_data["tasks"] = tasks
        return project_data
        
    def _collect_rules(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect project rules with retro UI."""
        rules = {"suggested": [], "custom": []}
        
        if self.use_claude and self.claude_setup:
            # Get Claude's suggestions
            self.ui.show_progress(
                "RULE GENERATION",
                "Claude is defining project standards...",
                "AI-powered best practices",
                [
                    "Analyzing technology stack",
                    "Defining coding standards",
                    "Setting quality guidelines"
                ]
            )
            
            claude_rules = self.claude_setup._get_claude_rule_suggestions(project_data)
            self.ui.stop_progress()
            
            if claude_rules:
                # Show rules summary
                rules_summary = "Claude recommends these project rules:\n\n"
                for i, rule in enumerate(claude_rules[:5], 1):
                    rules_summary += f"{i}. {rule}\n"
                if len(claude_rules) > 5:
                    rules_summary += f"\n...and {len(claude_rules) - 5} more rules"
                    
                use_suggested = self.ui.ask_confirm(
                    "CLAUDE RULES",
                    rules_summary,
                    default=True,
                    subtitle="AI Best Practices",
                    hint="Accept Claude's recommended standards"
                )
                
                if use_suggested:
                    rules["suggested"] = claude_rules[:10]
                    
        else:
            # Use standard suggestions
            suggested = self.project_config.project_types[
                project_data["metadata"]["project_type"]
            ]["suggested_rules"]
            
            if suggested:
                rules_summary = "Standard rules for your project type:\n\n"
                for i, rule in enumerate(suggested[:5], 1):
                    rules_summary += f"{i}. {rule}\n"
                    
                use_suggested = self.ui.ask_confirm(
                    "PROJECT RULES",
                    rules_summary,
                    default=True,
                    subtitle="Step 6 of 7"
                )
                
                if use_suggested:
                    rules["suggested"] = suggested
                    
        # Custom rules
        while self.ui.ask_confirm(
            "CUSTOM RULE",
            "Add a custom rule?",
            default=False,
            subtitle=f"Currently have {len(rules['suggested']) + len(rules['custom'])} rules"
        ):
            custom_rule = self.ui.ask_text(
                "ENTER RULE",
                "Enter custom rule:",
                subtitle="Define your standard"
            )
            
            if custom_rule:
                rules["custom"].append(custom_rule)
                
        project_data["rules"] = rules
        return project_data
        
    def _collect_additional_config(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect additional configuration with retro UI."""
        # Commands
        commands = {}
        
        if self.use_claude and self.claude_setup:
            self.ui.show_progress(
                "COMMAND GENERATION",
                "Claude is creating build commands...",
                "AI-powered automation"
            )
            
            claude_commands = self.claude_setup._get_claude_commands(project_data)
            self.ui.stop_progress()
            
            if claude_commands:
                # Show commands
                cmd_summary = "Claude suggests these commands:\n\n"
                for cmd, value in list(claude_commands.items())[:5]:
                    cmd_summary += f"• {cmd}: {value}\n"
                    
                use_commands = self.ui.ask_confirm(
                    "BUILD COMMANDS",
                    cmd_summary,
                    default=True,
                    subtitle="Step 7 of 7",
                    hint="Accept Claude's build configuration"
                )
                
                if use_commands:
                    commands = claude_commands
                    
        # Git setup
        git_init = self.ui.ask_confirm(
            "GIT REPOSITORY",
            "Initialize git repository?",
            default=True,
            subtitle="Version Control",
            hint="Set up git for your project"
        )
        
        if git_init:
            project_data["metadata"]["git"] = {
                "init": True,
                "initial_branch": "main"
            }
            
        project_data["metadata"]["commands"] = commands
        return project_data
        
    def _review_and_confirm(self, project_data: Dict[str, Any]) -> bool:
        """Review configuration and confirm with retro UI."""
        # Prepare summary
        summary = {
            "Project": project_data["project_name"],
            "Type": project_data["metadata"]["project_type_name"],
            "Language": project_data["metadata"]["language"],
            "Modules": len(project_data.get("modules", [])),
            "Tasks": len(project_data.get("tasks", [])),
            "Rules": len(project_data.get("rules", {}).get("suggested", [])) + 
                     len(project_data.get("rules", {}).get("custom", [])),
            "Claude Enhanced": "Yes" if project_data.get("enhanced_with_claude") else "No"
        }
        
        # Show summary
        action = self.ui.show_results(
            "CONFIGURATION REVIEW",
            summary,
            "Final Review",
            ["Proceed with setup", "Cancel setup"]
        )
        
        return action == "Proceed with setup"