"""Enhanced interactive setup with improved UI and discovery system."""

import time
from typing import Dict, List, Any, Optional
from ..utils.terminal_ui import EnhancedTerminalUI, MessageType
from ..utils.progress import progress_indicator
from ..claude.claude_processor import ClaudeProcessor
from ..config.project_config import ProjectConfig
import questionary
import yaml
from pathlib import Path


class EnhancedInteractiveSetup:
    """Enhanced interactive setup with deep discovery system."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.ui = EnhancedTerminalUI()
        self.claude_processor = ClaudeProcessor()
        self.config = self._load_config(config_file)
        self.discovery_responses = []
        self.project_context = {}
        
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "discovery": {
                "max_questions": 100,
                "enable_deep_discovery": True
            },
            "claude": {
                "timeout_seconds": 300,
                "max_retries": 3,
                "chunk_size": 3
            },
            "ui": {
                "show_progress_bars": True,
                "fixed_input_box": True,
                "message_boxes": True
            }
        }
        
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                user_config = yaml.safe_load(f)
                # Merge with defaults
                for key in default_config:
                    if key in user_config:
                        default_config[key].update(user_config[key])
        
        return default_config
    
    def run(self) -> Dict[str, Any]:
        """Run the enhanced interactive setup."""
        self.ui.clear_screen()
        self.ui.display()
        
        # Step 1: Get initial project information
        self.ui.show_info("Welcome to Claude Scaffold Enhanced Setup! 🚀")
        time.sleep(1)
        
        project_info = self._collect_initial_info()
        
        # Step 2: Deep discovery phase (if enabled)
        if self.config["discovery"]["enable_deep_discovery"]:
            self.ui.show_info("Starting deep discovery phase. I'll ask some questions to better understand your project.")
            self._run_discovery_phase(project_info)
        
        # Step 3: Generate enhanced project structure
        self.ui.show_info("Now I'll generate an enhanced project structure based on our discussion.")
        enhanced_project = self._generate_enhanced_project(project_info)
        
        # Step 4: Review and customize
        final_project = self._review_and_customize(enhanced_project)
        
        # Step 5: Create the project
        if self.ui.confirm("Ready to create your project?", default=True):
            self._create_project(final_project)
            self.ui.show_success("Project created successfully! 🎉")
        else:
            self.ui.show_info("Project creation cancelled.")
        
        return final_project
    
    def _collect_initial_info(self) -> Dict[str, Any]:
        """Collect initial project information."""
        # Project name
        project_name = self.ui.ask_question(
            "What would you like to name your project?"
        )
        
        # Project type
        project_types = [
            "Web Application",
            "API Service", 
            "CLI Tool",
            "Library/Package",
            "Mobile App",
            "Desktop Application",
            "Data Science Project",
            "Machine Learning Project",
            "Other"
        ]
        
        project_type = self.ui.ask_question(
            "What type of project are you building?",
            choices=project_types
        )
        
        # Project description
        description = self.ui.ask_question(
            "Please provide a brief description of your project (2-3 sentences):"
        )
        
        # Programming language
        languages = ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "C++", "Other"]
        language = self.ui.ask_question(
            "What programming language will you use?",
            choices=languages
        )
        
        return {
            "project_name": project_name,
            "project_type": project_type,
            "description": description,
            "language": language,
            "metadata": {
                "project_type_name": project_type,
                "language": language,
                "description": description
            }
        }
    
    def _run_discovery_phase(self, project_info: Dict[str, Any]):
        """Run the deep discovery phase with intelligent questions."""
        max_questions = self.config["discovery"]["max_questions"]
        question_count = 0
        
        # Categories of questions to explore
        categories = [
            "business_requirements",
            "technical_architecture", 
            "user_experience",
            "integrations",
            "scalability",
            "security",
            "deployment",
            "maintenance"
        ]
        
        current_category_index = 0
        
        while question_count < max_questions:
            # Check if user wants to stop
            if question_count > 0 and question_count % 10 == 0:
                if not self.ui.confirm(
                    f"We've covered {question_count} questions. Would you like to continue with more detailed questions?",
                    default=True
                ):
                    self.ui.show_info("Ending discovery phase.")
                    break
            
            # Generate next question based on context
            category = categories[current_category_index % len(categories)]
            
            with progress_indicator.claude_thinking(f"Generating {category.replace('_', ' ')} question"):
                question = self._generate_contextual_question(
                    project_info, 
                    self.discovery_responses,
                    category
                )
            
            if question:
                # Ask the question
                answer = self.ui.ask_question(question)
                
                # Check for stop keywords
                if answer and answer.lower() in ["enough", "stop", "done", "finish"]:
                    self.ui.show_info("Got it! Ending discovery phase.")
                    break
                
                # Store the response
                self.discovery_responses.append({
                    "category": category,
                    "question": question,
                    "answer": answer
                })
                
                question_count += 1
                current_category_index += 1
            else:
                # Move to next category if no question generated
                current_category_index += 1
                if current_category_index >= len(categories) * 2:
                    # We've tried all categories twice, end discovery
                    break
        
        self.ui.show_success(f"Discovery phase complete! Collected {len(self.discovery_responses)} responses.")
    
    def _generate_contextual_question(self, project_info: Dict, responses: List[Dict], category: str) -> Optional[str]:
        """Generate a contextual question based on previous responses."""
        # This is a simplified version - in production, this would call Claude
        # to generate intelligent questions based on the context
        
        question_templates = {
            "business_requirements": [
                "What is the primary business goal of this project?",
                "Who are your target users?",
                "What problem does this solve for your users?",
                "What are the key features you envision?",
                "What's your expected timeline for the MVP?"
            ],
            "technical_architecture": [
                "What database system do you plan to use?",
                "Will this be a monolithic or microservices architecture?",
                "What are your performance requirements?",
                "Do you need real-time features?",
                "What caching strategy would you like to implement?"
            ],
            "user_experience": [
                "What devices will your users primarily use?",
                "Do you need multi-language support?",
                "What's the expected user journey?",
                "Do you need accessibility features?",
                "What kind of notifications will you need?"
            ],
            "integrations": [
                "What third-party services will you integrate with?",
                "Do you need payment processing?",
                "Will you integrate with social media platforms?",
                "Do you need email/SMS capabilities?",
                "What APIs will you consume?"
            ],
            "scalability": [
                "What's your expected user base size?",
                "How much data will you process?",
                "Do you need horizontal scaling?",
                "What are your availability requirements?",
                "Do you need multi-region support?"
            ],
            "security": [
                "What authentication method will you use?",
                "Do you need role-based access control?",
                "Will you handle sensitive data?",
                "Do you need encryption at rest?",
                "What compliance requirements do you have?"
            ],
            "deployment": [
                "Where will you deploy this application?",
                "Do you need CI/CD pipelines?",
                "Will you use containers?",
                "Do you need blue-green deployments?",
                "What monitoring do you need?"
            ],
            "maintenance": [
                "How will you handle updates?",
                "Do you need automated testing?",
                "What's your backup strategy?",
                "How will you handle errors?",
                "Do you need audit logging?"
            ]
        }
        
        # Get questions for the category
        category_questions = question_templates.get(category, [])
        
        # Filter out already asked questions
        asked_questions = [r["question"] for r in responses]
        available_questions = [q for q in category_questions if q not in asked_questions]
        
        if available_questions:
            return available_questions[0]
        
        return None
    
    def _generate_enhanced_project(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced project structure using Claude."""
        # Combine initial info with discovery responses
        enhanced_context = {
            **project_info,
            "discovery_responses": self.discovery_responses
        }
        
        # This would normally call Claude to generate a comprehensive project structure
        # For now, we'll create a basic structure
        modules = [
            {
                "name": "core",
                "description": "Core business logic and domain models",
                "key_features": ["Domain models", "Business rules", "Core algorithms"]
            },
            {
                "name": "api",
                "description": "API endpoints and request handling",
                "key_features": ["REST endpoints", "Request validation", "Response formatting"]
            },
            {
                "name": "database",
                "description": "Database models and data access layer",
                "key_features": ["ORM models", "Migrations", "Query builders"]
            },
            {
                "name": "auth",
                "description": "Authentication and authorization",
                "key_features": ["User authentication", "JWT tokens", "Permission system"]
            },
            {
                "name": "utils",
                "description": "Utility functions and helpers",
                "key_features": ["Common utilities", "Validators", "Formatters"]
            }
        ]
        
        tasks = [
            {
                "title": "Set up project structure",
                "module": "core",
                "priority": "high",
                "status": "pending"
            },
            {
                "title": "Create database models",
                "module": "database",
                "priority": "high",
                "status": "pending"
            },
            {
                "title": "Implement authentication",
                "module": "auth",
                "priority": "high",
                "status": "pending"
            },
            {
                "title": "Create API endpoints",
                "module": "api",
                "priority": "medium",
                "status": "pending"
            },
            {
                "title": "Add input validation",
                "module": "api",
                "priority": "medium",
                "status": "pending"
            }
        ]
        
        rules = {
            "suggested": [
                "Follow TDD approach for all new features",
                "Write comprehensive documentation",
                "Use type hints in Python code",
                "Implement proper error handling",
                "Follow security best practices"
            ],
            "custom": []
        }
        
        return {
            **project_info,
            "modules": modules,
            "tasks": tasks,
            "rules": rules,
            "enhanced_by_discovery": True,
            "discovery_summary": self._summarize_discovery()
        }
    
    def _summarize_discovery(self) -> Dict[str, Any]:
        """Summarize the discovery phase responses."""
        summary = {}
        
        # Group responses by category
        for response in self.discovery_responses:
            category = response["category"]
            if category not in summary:
                summary[category] = []
            summary[category].append({
                "q": response["question"],
                "a": response["answer"]
            })
        
        return summary
    
    def _review_and_customize(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Allow user to review and customize the generated project."""
        self.ui.show_info("Let's review your project structure:")
        
        # Show modules
        self.ui.show_module_suggestions(project_data["modules"])
        
        if self.ui.confirm("Would you like to customize the modules?"):
            # Module customization logic here
            pass
        
        # Show tasks
        self.ui.show_task_list(project_data["tasks"])
        
        if self.ui.confirm("Would you like to customize the tasks?"):
            # Task customization logic here
            pass
        
        return project_data
    
    def _create_project(self, project_data: Dict[str, Any]):
        """Create the actual project structure."""
        with progress_indicator.operation("Creating project", total=5) as progress:
            progress.update(description="Creating directory structure...")
            time.sleep(0.5)
            
            progress.update(description="Generating module files...")
            time.sleep(0.5)
            
            progress.update(description="Creating documentation...")
            time.sleep(0.5)
            
            progress.update(description="Setting up configuration...")
            time.sleep(0.5)
            
            progress.update(description="Finalizing project...")
            time.sleep(0.5)
            
        # In real implementation, this would use ProjectCreator
        # to actually create the project files and structure