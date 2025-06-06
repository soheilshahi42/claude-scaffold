"""Project configuration and type definitions."""


class ProjectConfig:
    """Manages project type configurations and defaults."""

    def __init__(self):
        self.project_types = {
            "web": {
                "name": "Web Application",
                "description": "Full-stack or frontend web application",
                "suggested_modules": ["frontend", "backend", "api", "database", "auth"],
                "suggested_rules": [
                    "Follow React/Vue/Angular best practices",
                    "Use TypeScript for type safety",
                    "Implement responsive design",
                    "Follow REST/GraphQL API conventions",
                ],
                "test_framework": "jest/pytest",
                "build_commands": ["npm install", "npm run build", "npm test"],
            },
            "cli": {
                "name": "Command Line Tool",
                "description": "CLI application or utility",
                "suggested_modules": ["commands", "utils", "config", "output"],
                "suggested_rules": [
                    "Follow POSIX conventions",
                    "Provide helpful error messages",
                    "Support both interactive and non-interactive modes",
                    "Include comprehensive --help documentation",
                ],
                "test_framework": "pytest",
                "build_commands": ["pip install -e .", "pytest", "mypy ."],
            },
            "library": {
                "name": "Python Library",
                "description": "Reusable Python package",
                "suggested_modules": ["core", "utils", "exceptions", "types"],
                "suggested_rules": [
                    "Follow PEP 8 style guide",
                    "Provide comprehensive docstrings",
                    "Include type hints",
                    "Maintain backward compatibility",
                ],
                "test_framework": "pytest",
                "build_commands": [
                    "pip install -e .[dev]",
                    "pytest",
                    "black .",
                    "mypy .",
                ],
            },
            "api": {
                "name": "API Service",
                "description": "REST or GraphQL API service",
                "suggested_modules": [
                    "routes",
                    "models",
                    "services",
                    "middleware",
                    "auth",
                ],
                "suggested_rules": [
                    "Follow OpenAPI/Swagger specifications",
                    "Implement proper versioning",
                    "Use consistent error responses",
                    "Include rate limiting",
                ],
                "test_framework": "pytest",
                "build_commands": [
                    "pip install -r requirements.txt",
                    "pytest",
                    "uvicorn main:app --reload",
                ],
            },
            "ml": {
                "name": "Machine Learning Project",
                "description": "ML/Data Science project",
                "suggested_modules": [
                    "data",
                    "models",
                    "training",
                    "evaluation",
                    "utils",
                ],
                "suggested_rules": [
                    "Version control data and models",
                    "Implement reproducible experiments",
                    "Document model architecture",
                    "Track metrics and experiments",
                ],
                "test_framework": "pytest",
                "build_commands": [
                    "pip install -r requirements.txt",
                    "pytest",
                    "python train.py",
                ],
            },
            "custom": {
                "name": "Custom Project",
                "description": "Define your own project structure",
                "suggested_modules": ["core"],
                "suggested_rules": [],
                "test_framework": "pytest",
                "build_commands": ["pip install -e .", "pytest"],
            },
        }

        self.style_guides = {
            "pep8": "PEP 8 Style Guide",
            "black": "Black Code Formatter",
            "google": "Google Python Style Guide",
            "custom": "Custom style guide",
        }

        self.test_frameworks = {
            "pytest": "pytest - Python testing framework",
            "unittest": "unittest - Python standard library",
            "jest": "Jest - JavaScript testing framework",
            "mocha": "Mocha - JavaScript test framework",
            "custom": "Custom testing framework",
        }

    def get_suggested_tasks(self, project_type: str) -> list:
        """Get suggested tasks based on project type."""
        tasks = {
            "web": [
                "Set up development environment",
                "Design database schema",
                "Implement user authentication",
                "Create main UI components",
                "Set up API endpoints",
                "Implement frontend routing",
                "Add form validation",
                "Set up deployment pipeline",
            ],
            "cli": [
                "Define command structure",
                "Implement argument parsing",
                "Create configuration system",
                "Add output formatting",
                "Implement main command logic",
                "Add logging system",
                "Create help documentation",
                "Add shell completion",
            ],
            "library": [
                "Define public API",
                "Implement core functionality",
                "Add type hints",
                "Write comprehensive tests",
                "Create usage examples",
                "Set up documentation",
                "Configure package distribution",
                "Add CI/CD pipeline",
            ],
            "api": [
                "Design API endpoints",
                "Set up database models",
                "Implement authentication",
                "Create request validation",
                "Add error handling",
                "Implement rate limiting",
                "Set up API documentation",
                "Add monitoring/logging",
            ],
            "ml": [
                "Set up data pipeline",
                "Implement data preprocessing",
                "Design model architecture",
                "Create training loop",
                "Implement evaluation metrics",
                "Add experiment tracking",
                "Create prediction pipeline",
                "Document model performance",
            ],
            "custom": [],
        }
        return tasks.get(project_type, [])
