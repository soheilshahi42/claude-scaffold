"""Core Claude processing functionality."""

import json
import subprocess
from typing import Any, Callable, Dict, List, Optional

from ..utils.logger import get_logger
from ..utils.progress import progress_indicator
from .claude_task_queue import ClaudeTaskQueue
from .prompts import (
    PROJECT_SETUP_ENHANCEMENT_PROMPT,
    TASK_DETAILS_GENERATION_PROMPT,
    MODULE_DOCUMENTATION_ENHANCEMENT_PROMPT,
    MODULE_DOCUMENTATION_REFINEMENT_PROMPT,
    GLOBAL_RULES_GENERATION_PROMPT,
    PROJECT_CONFIGURATION_VALIDATION_PROMPT,
    MODULE_DESCRIPTION_BATCH_PROMPT,
    TASK_DETAILS_BATCH_PROMPT,
    PROJECT_QUESTIONS_INITIAL_PROMPT,
    PROJECT_QUESTIONS_CONTEXTUAL_PROMPT,
    QA_COMPILATION_TO_SPEC_PROMPT
)


class ClaudeProcessor:
    """Process user inputs through Claude in headless mode."""

    def __init__(self, debug_mode: bool = False, timeout: int = 300, max_retries: int = 3):
        self.claude_executable = "claude"  # Assumes claude is in PATH
        self.logger = get_logger(debug_mode)
        self.default_timeout = timeout  # Default 5 minutes
        self.max_retries = max_retries  # Maximum retry attempts

    def process_project_setup(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process project setup through Claude to generate intelligent configuration."""

        with progress_indicator.claude_thinking("Analyzing your project requirements") as progress:
            # Prepare the configuration JSON for the prompt
            config_json = json.dumps(initial_data, indent=2)
            
            # Use the imported prompt template
            prompt = PROJECT_SETUP_ENHANCEMENT_PROMPT.format(
                config_json=config_json
            )

            progress.update_status("Preparing prompt", "Initialization")
            progress.set_prompt_size(len(prompt))

            progress.update_status("Calling Claude API", "Processing")
            response = self._call_claude(prompt, progress_callback=progress.update_status)

            progress.update_status("Parsing response", "Finalizing")
            claude_config = json.loads(response)

            # Merge Claude's enhancements with original data
            progress.update_status("Merging configurations", "Finalizing")
            enhanced_data = self._merge_claude_config(initial_data, claude_config)

        return enhanced_data

    def generate_task_details(
        self, task_title: str, module_name: str, project_context: Dict
    ) -> Dict[str, Any]:
        """Generate detailed task specifications using Claude."""

        with progress_indicator.claude_thinking(
            f"Generating details for task: {task_title}"
        ) as progress:
            # Use the imported prompt template
            prompt = TASK_DETAILS_GENERATION_PROMPT.format(
                task_name=task_title,
                module_name=module_name,
                project_type=project_context['metadata']['project_type_name'],
                language=project_context['metadata']['language']
            )

            progress.set_prompt_size(len(prompt))
            progress.update_status("Calling Claude API", "Processing")
            response = self._call_claude(prompt, progress_callback=progress.update_status)

            progress.update_status("Parsing task details", "Finalizing")
            return json.loads(response)

    def enhance_module_documentation(self, module: Dict, project_context: Dict, allow_feedback: bool = True) -> Dict[str, Any]:
        """Generate enhanced module documentation using Claude with optional feedback."""
        import questionary
        from ..utils.icons import icons
        
        with progress_indicator.claude_thinking(
            f"Enhancing documentation for module: {module['name']}"
        ) as progress:
            # Get list of other modules
            other_modules = [m['name'] for m in project_context.get('modules', []) if m['name'] != module['name']]
            
            # Use the imported prompt template
            prompt = MODULE_DOCUMENTATION_ENHANCEMENT_PROMPT.format(
                module_name=module['name'],
                description=module['description'],
                project_type=project_context['metadata']['project_type_name'],
                language=project_context['metadata']['language'],
                other_modules=', '.join(other_modules) if other_modules else 'None'
            )

            progress.set_prompt_size(len(prompt))
            progress.update_status("Calling Claude API", "Processing")
            response = self._call_claude(prompt, progress_callback=progress.update_status)

            progress.update_status("Parsing module documentation", "Finalizing")
            documentation = json.loads(response)
            
        if allow_feedback:
            # Show summary of generated documentation
            print(f"\n{icons.MODULE} Generated documentation for {module['name']}:")
            if 'responsibilities' in documentation:
                print(f"   Responsibilities: {documentation['responsibilities'][:100]}...")
            if 'public_api' in documentation:
                print(f"   API suggestions: {len(documentation.get('public_api', []))} items")
                
            # Ask for feedback
            refine = questionary.confirm(
                f"\n{icons.QUESTION} Would you like to refine this documentation?",
                default=False
            ).ask()
            
            if refine:
                max_iterations = 3
                for iteration in range(max_iterations):
                    feedback = questionary.text(
                        "Your feedback for improvement:",
                        multiline=True
                    ).ask()
                    
                    if not feedback:
                        break
                        
                    # Refine with feedback using the imported prompt
                    refine_prompt = MODULE_DOCUMENTATION_REFINEMENT_PROMPT.format(
                        current_doc=json.dumps(documentation),
                        feedback=feedback
                    )
                    
                    try:
                        print(f"\n{icons.ROBOT} Refining documentation...")
                        refined_response = self._call_claude(refine_prompt)
                        documentation = json.loads(refined_response)
                        
                        print(f"{icons.SUCCESS} Documentation refined!")
                        if 'responsibilities' in documentation:
                            print(f"   New responsibilities: {documentation['responsibilities'][:100]}...")
                            
                        if iteration < max_iterations - 1:
                            continue_refining = questionary.confirm(
                                "Continue refining?",
                                default=False
                            ).ask()
                            if not continue_refining:
                                break
                    except Exception as e:
                        print(f"{icons.WARNING} Refinement failed: {e}")
                        break
                        
        return documentation

    def generate_global_rules(self, project_data: Dict) -> List[str]:
        """Generate project-specific global rules using Claude."""

        with progress_indicator.claude_thinking("Generating project-specific rules") as progress:
            # Use the imported prompt template
            prompt = GLOBAL_RULES_GENERATION_PROMPT.format(
                config=json.dumps(project_data, indent=2),
                language=project_data['metadata']['language'],
                project_type=project_data['metadata']['project_type_name']
            )

            progress.set_prompt_size(len(prompt))
            progress.update_status("Calling Claude API", "Processing")
            response = self._call_claude(prompt, progress_callback=progress.update_status)

            progress.update_status("Parsing generated rules", "Finalizing")
            return json.loads(response)

    def validate_project_configuration(self, project_data: Dict) -> Dict[str, Any]:
        """Validate and suggest improvements for project configuration."""

        with progress_indicator.claude_thinking("Validating project configuration") as progress:
            # Use the imported prompt template
            prompt = PROJECT_CONFIGURATION_VALIDATION_PROMPT.format(
                config_json=json.dumps(project_data, indent=2)
            )

            progress.set_prompt_size(len(prompt))
            progress.update_status("Calling Claude API", "Processing")
            response = self._call_claude(prompt, progress_callback=progress.update_status)

            progress.update_status("Parsing validation results", "Finalizing")
            return json.loads(response)

    def _call_claude(
        self,
        prompt: str,
        timeout: Optional[int] = None,
        expect_json: bool = True,
        progress_callback: Optional[Callable] = None,
    ) -> str:
        """Call Claude in headless mode with a prompt, with retry logic."""
        if timeout is None:
            timeout = self.default_timeout

        self.logger.debug(
            "Preparing Claude call", {"prompt_length": len(prompt), "timeout": timeout}
        )

        # Add system prompt for better JSON generation (only if expecting JSON)
        if expect_json:
            system_prompt = (
                "You are a helpful assistant that generates structured JSON responses for "
                "software project configuration. Always respond with valid JSON that matches "
                "the requested schema. Do not include any markdown formatting or code blocks - "
                "just the raw JSON."
            )
            # Combine system prompt with user prompt since Claude CLI doesn't
            # support separate system prompts
            full_prompt = f"{system_prompt}\n\n{prompt}"
        else:
            full_prompt = prompt

        # Retry logic with exponential backoff
        last_error = None
        for attempt in range(self.max_retries):
            try:
                # Call Claude in non-interactive mode with combined prompt
                cmd = [
                    self.claude_executable,
                    "-p",  # Print mode (non-interactive)
                    full_prompt,
                ]
                
                # Note: Claude Code CLI doesn't support max-tokens in print mode
                # We rely on concise prompts to get reasonable response lengths

                if attempt > 0:
                    # Exponential backoff: 2^attempt seconds (2s, 4s, 8s...)
                    wait_time = 2**attempt
                    progress_indicator.show_retry(attempt + 1, self.max_retries, wait_time)

                if progress_callback:
                    progress_callback(
                        f"Calling Claude (attempt {attempt + 1}/{self.max_retries})",
                        "API Call",
                    )

                self.logger.debug(
                    "Executing Claude command",
                    {"command": cmd[:2] + ["..."], "attempt": attempt + 1},
                )

                import time as time_module

                start_time = time_module.time()

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

                duration = time_module.time() - start_time
                self.logger.log_performance(
                    f"Claude API call (attempt {attempt + 1})",
                    duration,
                    result.returncode == 0,
                )

                self.logger.log_claude_interaction(
                    prompt=prompt,
                    response=result.stdout,
                    error=(None if result.returncode == 0 else RuntimeError(result.stderr)),
                    command=cmd[:2] + ["..."],
                )

                if result.returncode != 0:
                    error = RuntimeError(f"Claude returned error: {result.stderr}")
                    self.logger.error("Claude command failed", error)
                    raise error

                response = result.stdout.strip()

                # Try to clean the response if it contains markdown
                if "```json" in response:
                    json_start = response.find("```json") + 7
                    json_end = response.find("```", json_start)
                    if json_end > json_start:
                        response = response[json_start:json_end].strip()
                        self.logger.debug("Extracted JSON from markdown block")
                elif "```" in response:
                    json_start = response.find("```") + 3
                    json_end = response.find("```", json_start)
                    if json_end > json_start:
                        response = response[json_start:json_end].strip()
                        self.logger.debug("Extracted content from code block")

                # Validate it's proper JSON (only if expecting JSON)
                if expect_json:
                    try:
                        json.loads(response)
                        self.logger.debug("Claude response is valid JSON")
                    except json.JSONDecodeError as e:
                        self.logger.log_json_parse_error(response, e)
                        self.logger.warning("Claude response is not valid JSON, returning raw")

                # Success! Return the response
                return response

            except subprocess.TimeoutExpired as e:
                last_error = e
                self.logger.warning(
                    f"Claude call timed out after {timeout}s "
                    f"(attempt {attempt + 1}/{self.max_retries})"
                )
                if attempt < self.max_retries - 1:
                    self.logger.info("Timeout occurred, retrying...")
                continue

            except Exception as e:
                last_error = e
                self.logger.warning(
                    f"Failed to call Claude (attempt {attempt + 1}/{self.max_retries}): {str(e)}"
                )
                if attempt < self.max_retries - 1:
                    continue
                break

        # All retries failed
        self.logger.error(f"All {self.max_retries} attempts to call Claude failed", last_error)
        if isinstance(last_error, subprocess.TimeoutExpired):
            progress_indicator.show_error(
                f"Claude call timed out after {timeout} seconds (tried {self.max_retries} times)",
                "Try breaking your request into smaller parts or increasing the timeout setting.",
            )
            raise RuntimeError(
                f"Claude call timed out after {timeout} seconds (tried {self.max_retries} times)"
            )
        else:
            progress_indicator.show_error(
                f"Failed to call Claude after {self.max_retries} attempts: {str(last_error)}",
                "Check your Claude CLI installation and ensure it's properly configured.",
            )
            raise RuntimeError(
                f"Failed to call Claude after {self.max_retries} attempts: {str(last_error)}"
            )

    def _merge_claude_config(self, original_data: Dict, claude_config: Dict) -> Dict[str, Any]:
        """Merge Claude's enhancements with original data."""
        enhanced_data = original_data.copy()

        # Update description
        if "enhanced_description" in claude_config:
            enhanced_data["metadata"]["description"] = claude_config["enhanced_description"]

        # Enhance modules
        if "module_enhancements" in claude_config:
            for module in enhanced_data["modules"]:
                if module["name"] in claude_config["module_enhancements"]:
                    module["documentation"] = claude_config["module_enhancements"][module["name"]]

        # Enhance tasks
        if "task_details" in claude_config:
            for task in enhanced_data["tasks"]:
                if task["title"] in claude_config["task_details"]:
                    task["details"] = claude_config["task_details"][task["title"]]

        # Add additional rules
        if "additional_rules" in claude_config:
            enhanced_data["rules"]["suggested"].extend(claude_config["additional_rules"])

        # Add other enhancements
        for key in [
            "architecture_recommendations",
            "testing_strategy",
            "security_considerations",
            "performance_guidelines",
        ]:
            if key in claude_config:
                enhanced_data["metadata"][key] = claude_config[key]

        return enhanced_data

    def _format_modules(self, modules: List[Dict]) -> str:
        """Format modules for prompt."""
        return "\n".join([f"- {m['name']}: {m['description']}" for m in modules])

    def _format_tasks(self, tasks: List[Dict]) -> str:
        """Format tasks for prompt."""
        return "\n".join(
            [f"- [{t['module']}] {t['title']} (Priority: {t['priority']})" for t in tasks]
        )

    def _format_rules(self, rules: Dict) -> str:
        """Format rules for prompt."""
        all_rules = rules.get("suggested", []) + rules.get("custom", [])
        if not all_rules:
            return "No existing rules"
        return "\n".join([f"- {rule}" for rule in all_rules])

    def _format_list(self, items: List[str]) -> str:
        """Format a list for prompt."""
        if not items:
            return "None"
        return "\n".join([f"- {item}" for item in items])

    def generate_module_descriptions_batch(
        self, modules: List[str], project_context: Dict
    ) -> Dict[str, str]:
        """Generate descriptions for multiple modules concurrently.

        Args:
            modules: List of module names
            project_context: Project context information

        Returns:
            Dictionary mapping module names to descriptions
        """
        self.logger.info(f"Generating descriptions for {len(modules)} modules concurrently")

        # Create task queue with exactly 3 workers
        task_queue = ClaudeTaskQueue(
            max_workers=3, debug_mode=self.logger.debug_mode
        )

        # Add tasks for each module
        for module in modules:
            project_type = project_context["metadata"]["project_type_name"]
            prompt = (
                f"""Generate a concise description for the '{module}' module """
                f"""in a {project_type} project.

Project: {project_context['project_name']}
Description: {project_context['metadata']['description']}
Language: {project_context['metadata']['language']}

Provide a 1-2 sentence description that clearly explains the module's purpose
and key responsibilities."""
            )

            task_queue.add_task(
                task_id=module,
                name=f"Module: {module}",
                prompt=prompt,
                expect_json=False,
                timeout=90,  # 90 second timeout to allow for comprehensive descriptions
            )

        # Process all tasks
        results = task_queue.process_tasks(self)

        # Convert results to module descriptions
        descriptions = {}
        for module, description in results.items():
            if description:
                descriptions[module] = description.strip()
            else:
                # Fallback description if Claude fails
                descriptions[module] = f"{module.title()} module functionality"

        return descriptions

    def generate_task_details_batch(
        self, tasks: List[Dict], project_context: Dict, allow_feedback: bool = True
    ) -> Dict[str, Dict]:
        """Generate details for multiple tasks concurrently with optional feedback.

        Args:
            tasks: List of task dictionaries with title and module
            project_context: Project context information
            allow_feedback: Whether to allow user feedback on generated details

        Returns:
            Dictionary mapping task titles to task details
        """
        import questionary
        from ..utils.icons import icons
        
        self.logger.info(f"Generating details for {len(tasks)} tasks concurrently")

        # Create task queue
        task_queue = ClaudeTaskQueue(
            max_workers=min(3, len(tasks)), debug_mode=self.logger.debug_mode
        )

        # Add tasks
        for task in tasks:
            prompt = f"""Generate comprehensive task details for the following task:

Task: {task['title']}
Module: {task['module']}
Project Type: {project_context['metadata']['project_type_name']}
Project Description: {project_context['metadata']['description']}

Please provide:
1. Clear goal statement
2. Key requirements (3-5 items)
3. Recommended implementation approach
4. Specific subtasks following TDD methodology (5-8 items)
5. Acceptance criteria
6. Potential challenges
7. Research topics

Return as JSON with keys: goal, requirements, approach, subtasks, acceptance_criteria,
challenges, research_topics"""

            task_queue.add_task(
                task_id=task["title"],
                name=f"Task: {task['title']}",
                prompt=prompt,
                expect_json=True,
                timeout=120,
            )

        # Process all tasks
        results = task_queue.process_tasks(self)

        # Convert results
        task_details = {}
        for title, details in results.items():
            if details:
                try:
                    task_details[title] = (
                        json.loads(details) if isinstance(details, str) else details
                    )
                except Exception:
                    task_details[title] = {"error": "Failed to parse details"}
            else:
                task_details[title] = {"error": "No details generated"}
                
        if allow_feedback and task_details:
            # Show summary of generated task details
            print(f"\n{icons.TASK} Generated details for {len(task_details)} tasks:")
            for i, (title, details) in enumerate(list(task_details.items())[:5], 1):
                if 'error' not in details:
                    goal = details.get('goal', 'No goal defined')[:80]
                    print(f"   {i}. {title}")
                    print(f"      Goal: {goal}...")
            
            if len(task_details) > 5:
                print(f"   ... and {len(task_details) - 5} more tasks")
                
            # Ask if user wants to refine any tasks
            refine = questionary.confirm(
                f"\n{icons.QUESTION} Would you like to refine any task details?",
                default=False
            ).ask()
            
            if refine:
                # Let user select which tasks to refine
                task_choices = []
                for title in task_details.keys():
                    if 'error' not in task_details[title]:
                        task_choices.append(title)
                        
                if task_choices:
                    tasks_to_refine = questionary.checkbox(
                        "Select tasks to refine:",
                        choices=task_choices[:10]  # Limit to 10 for UI
                    ).ask()
                    
                    for task_title in tasks_to_refine:
                        print(f"\n{icons.DOCUMENT} Refining task: {task_title}")
                        current_details = task_details[task_title]
                        
                        # Show current details
                        print(f"   Current goal: {current_details.get('goal', 'N/A')}")
                        print(f"   Subtasks: {len(current_details.get('subtasks', []))} items")
                        
                        feedback = questionary.text(
                            "Your feedback for this task:",
                            multiline=True
                        ).ask()
                        
                        if feedback:
                            # Find the original task
                            original_task = next((t for t in tasks if t['title'] == task_title), None)
                            if original_task:
                                refine_prompt = f"""Refine these task details based on user feedback:

Task: {task_title}
Module: {original_task['module']}
Current details: {json.dumps(current_details)}
User feedback: {feedback}

Return improved task details as JSON with the same structure."""
                                
                                try:
                                    print(f"{icons.ROBOT} Refining task details...")
                                    refined_response = self._call_claude(refine_prompt)
                                    task_details[task_title] = json.loads(refined_response)
                                    print(f"{icons.SUCCESS} Task details refined!")
                                except Exception as e:
                                    print(f"{icons.WARNING} Refinement failed: {e}")

        return task_details
    
    def generate_project_questions(self, project_description: str, existing_qa: List[Dict] = None) -> List[Dict[str, str]]:
        """Generate intelligent questions about the project.
        
        This method analyzes previous Q&A exchanges to generate contextual follow-up questions,
        ensuring a coherent conversation flow that builds upon already gathered information.
        """
        if existing_qa:
            # Generate follow-up questions based on existing Q&A history
            qa_context = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in existing_qa[-10:]])  # Use last 10 Q&As for context
            prompt = f"""
Based on this project description: "{project_description}"

And the conversation history from our Q&A session:
{qa_context}

Analyze what we've learned so far and generate 5 detailed follow-up questions that:
1. Build upon the previous answers
2. Explore areas that need more clarification
3. Dig deeper into technical decisions mentioned
4. Address any gaps or inconsistencies
5. Help complete the project specification

Focus on uncovering important details that haven't been fully addressed yet.
Consider the context of previous questions to avoid repetition.

Format each question exactly as:
CATEGORY: question text

Categories: TECHNICAL, FEATURES, ARCHITECTURE, DEPLOYMENT, USERS, CONSTRAINTS, INTEGRATIONS
"""
        else:
            # Generate initial questions for first round
            prompt = f"""
Given this project description: "{project_description}"

Generate exactly 25 detailed questions to understand the project better.
These should be initial discovery questions that help establish:
- Technical requirements (languages, frameworks, databases)
- Features and functionality
- Target users and use cases
- Deployment and hosting
- Integrations and APIs
- Performance and scalability needs
- Security requirements
- Development constraints

Make questions specific and actionable, not generic.

Format each question exactly as:
CATEGORY: question text

Categories: TECHNICAL, FEATURES, ARCHITECTURE, DEPLOYMENT, USERS, CONSTRAINTS, INTEGRATIONS
"""
        
        response = self._call_claude(prompt, expect_json=False, progress_callback=None)
        
        # Parse questions from response
        questions = []
        for line in response.strip().split('\n'):
            if ':' in line and any(cat in line.upper() for cat in ['TECHNICAL', 'FEATURES', 'ARCHITECTURE', 'DEPLOYMENT', 'USERS', 'CONSTRAINTS', 'INTEGRATIONS']):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    category = parts[0].strip().upper()
                    question = parts[1].strip()
                    # Only add if it's a valid category and question
                    if category in ['TECHNICAL', 'FEATURES', 'ARCHITECTURE', 'DEPLOYMENT', 'USERS', 'CONSTRAINTS', 'INTEGRATIONS'] and question:
                        questions.append({
                            'category': category,
                            'question': question
                        })
        
        return questions
    
    def compile_qa_into_spec(self, project_description: str, qa_session: List[Dict]) -> str:
        """Compile Q&A session into comprehensive project specification.
        
        Takes the full conversation history and creates a coherent technical specification
        that incorporates all the details gathered through the Q&A process.
        """
        # Create a structured Q&A text with categories
        qa_by_category = {}
        for qa in qa_session:
            category = qa.get('category', 'GENERAL')
            if category not in qa_by_category:
                qa_by_category[category] = []
            qa_by_category[category].append(f"Q: {qa['question']}\nA: {qa['answer']}")
        
        # Format Q&A by category for better context
        categorized_qa = []
        for category, items in qa_by_category.items():
            categorized_qa.append(f"\n## {category}\n")
            categorized_qa.extend(items)
        
        qa_text = "\n\n".join(categorized_qa)
        
        # Use the imported prompt template
        prompt = QA_COMPILATION_TO_SPEC_PROMPT.format(
            project_description=project_description,
            qa_text=qa_text
        )
        
        return self._call_claude(prompt, expect_json=False, timeout=300)  # Longer timeout for comprehensive spec
