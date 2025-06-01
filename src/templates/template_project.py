"""Project-specific templates."""

from typing import Dict


class ProjectSpecificTemplates:
    """Templates for project configuration files."""
    
    @staticmethod
    def get_templates() -> Dict[str, str]:
        """Return project-specific templates."""
        return {
            'claude_settings': """{{
  "tools": {{
    "file_operations": true,
    "bash_commands": true,
    "web_browser": false,
    "code_execution": true
  }},
  "context": {{
    "include_patterns": [
      "**/*.py",
      "**/*.md",
      "**/*.yaml",
      "**/*.yml",
      "**/*.json",
      "**/Dockerfile",
      "**/*.sh"
    ],
    "exclude_patterns": [
      "**/__pycache__/**",
      "**/*.pyc",
      "**/venv/**",
      "**/env/**",
      "**/.git/**",
      "**/node_modules/**",
      "**/dist/**",
      "**/build/**"
    ]
  }},
  "workflows": {{
    "task_implementation": {{
      "steps": [
        "Read task details in module CLAUDE.md",
        "Review/update research in docs/",
        "Write failing tests",
        "Implement solution",
        "Verify tests pass",
        "Update documentation"
      ]
    }},
    "code_review": {{
      "checklist": [
        "Tests pass",
        "Code follows style guide",
        "Documentation updated",
        "No security issues",
        "Performance considered"
      ]
    }}
  }}
}}
""",

            'gitignore': """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.tox/
.coverage
.coverage.*
.cache
.pytest_cache/
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~
.project
.pydevproject

# OS
.DS_Store
Thumbs.db

# Claude
CLAUDE.local.md
.claude/cache/

# Project specific
{project_specific_ignores}
"""
        }