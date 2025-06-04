"""Command templates for Claude Scaffold projects."""

from typing import Dict


class CommandTemplates:
    """Templates for custom Claude commands."""
    
    @staticmethod
    def get_templates() -> Dict[str, str]:
        """Return all command templates."""
        return {
            'test_command': '''#!/usr/bin/env python3
"""Custom test command for Claude Code."""
import subprocess
import sys

def main():
    """Run project tests with coverage."""
    print(f"{icons.BUILD} Running tests with coverage...")
    
    cmd = ["{test_command}"]
    if "--coverage" not in "{test_command}":
        # Add coverage if not already included
        cmd.extend(["--cov={project_name}", "--cov-report=term-missing"])
    
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print(f"{icons.SUCCESS} All tests passed!")
    else:
        print(f"{icons.ERROR} Some tests failed.")
    
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
''',

            'build_command': '''#!/usr/bin/env python3
"""Custom build command for Claude Code."""
import subprocess
import sys

def main():
    """Run project build process."""
    print(f"{icons.BUILD} Building project...")
    
    # Run build command
    build_cmd = "{build_command}".split()
    result = subprocess.run(build_cmd, capture_output=False)
    
    if result.returncode != 0:
        print(f"{icons.ERROR} Build failed!")
        sys.exit(result.returncode)
    
    # Run tests after build
    print("\\n{icons.BUILD} Running tests...")
    test_cmd = "{test_command}".split()
    result = subprocess.run(test_cmd, capture_output=False)
    
    if result.returncode == 0:
        print("\\n{icons.SUCCESS} Build successful and all tests passed!")
    else:
        print("\\n{icons.WARNING}  Build succeeded but some tests failed.")
    
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
''',

            'dev_command': '''#!/usr/bin/env python3
"""Custom development command for Claude Code."""
import subprocess
import sys
from ..utils.icons import icons

def main():
    """Start development environment."""
    print(f"{icons.ROCKET} Starting development environment...")
    
    cmd = "{dev_command}".split()
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(ff"{icons.ERROR} Development server failed: {{e}}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\\n👋 Development server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
''',

            'claude_init_tasks': '''#!/usr/bin/env python3
"""Initialize task list from CLAUDE.md for Claude Code development."""
import json
import re
from pathlib import Path
import sys


def parse_claude_md():
    """Parse CLAUDE.md and extract project information and tasks."""
    claude_file = Path("CLAUDE.md")
    
    if not claude_file.exists():
        print("❌ CLAUDE.md not found in current directory")
        return None
    
    content = claude_file.read_text()
    
    # Extract project name
    project_match = re.search(r'^#\\s+(.+?)\\s+Claude Documentation', content, re.MULTILINE)
    project_name = project_match.group(1) if project_match else "Project"
    
    # Extract modules and their tasks
    modules = {{}}
    current_module = None
    
    # Look for module sections
    module_pattern = r'^##\\s+Modules?\\s*$'
    if re.search(module_pattern, content, re.MULTILINE):
        # Extract module information
        lines = content.split('\\n')
        in_modules = False
        
        for line in lines:
            if re.match(module_pattern, line):
                in_modules = True
                continue
            elif in_modules and line.startswith('##'):
                break
            elif in_modules and line.strip().startswith('-'):
                # Parse module entry
                module_match = re.match(r'-\\s+\\*\\*(.+?)\\*\\*:\\s+(.+)', line.strip())
                if module_match:
                    module_name = module_match.group(1)
                    module_desc = module_match.group(2)
                    modules[module_name] = {{
                        'description': module_desc,
                        'tasks': []
                    }}
    
    # Look for tasks in TASKS.md if it exists
    tasks_file = Path("TASKS.md")
    if tasks_file.exists():
        tasks_content = tasks_file.read_text()
        
        # Parse tasks by module
        current_module = None
        lines = tasks_content.split('\\n')
        
        for line in lines:
            # Check for module headers
            if line.startswith('###') and not line.startswith('####'):
                module_match = re.match(r'^###\\s+(.+)', line)
                if module_match:
                    current_module = module_match.group(1).strip()
            # Check for task items
            elif line.strip().startswith('-') and current_module:
                task_match = re.match(r'-\\s+\\[(.+?)\\]\\s+(.+)', line.strip())
                if task_match:
                    priority = task_match.group(1)
                    task_desc = task_match.group(2)
                    
                    # Map priority indicators
                    priority_map = {{
                        '🔴': 'high',
                        '🟡': 'medium',
                        '🟢': 'low',
                        'High': 'high',
                        'Medium': 'medium',
                        'Low': 'low'
                    }}
                    
                    priority_level = priority_map.get(priority, 'medium')
                    
                    if current_module in modules:
                        modules[current_module]['tasks'].append({{
                            'description': task_desc,
                            'priority': priority_level,
                            'status': 'pending'
                        }})
    
    return {{
        'project_name': project_name,
        'modules': modules
    }}


def create_todo_list(project_data):
    """Create a structured TODO list for Claude Code."""
    todos = []
    
    # Add project setup task
    todos.append({{
        "id": "setup-001",
        "content": f"Review project structure and requirements for {{project_data['project_name']}}",
        "status": "pending",
        "priority": "high"
    }})
    
    # Add tasks for each module
    task_id = 1
    for module_name, module_info in project_data['modules'].items():
        # Add module setup task
        todos.append({{
            "id": f"{{module_name}}-setup",
            "content": f"Set up {{module_name}} module: {{module_info['description']}}",
            "status": "pending",
            "priority": "high"
        }})
        
        # Add module tasks
        for task in module_info['tasks']:
            todos.append({{
                "id": f"{{module_name}}-{{task_id:03d}}",
                "content": f"[{{module_name}}] {{task['description']}}",
                "status": task['status'],
                "priority": task['priority']
            }})
            task_id += 1
    
    # Add completion task
    todos.append({{
        "id": "final-001",
        "content": "Run final tests and ensure all modules integrate correctly",
        "status": "pending",
        "priority": "high"
    }})
    
    return todos


def main():
    """Main function to initialize Claude Code task list."""
    print("🚀 Initializing Claude Code task list from CLAUDE.md...")
    
    # Parse project information
    project_data = parse_claude_md()
    if not project_data:
        sys.exit(1)
    
    # Create TODO list
    todos = create_todo_list(project_data)
    
    # Display summary
    print(f"\\n📋 Project: {{project_data['project_name']}}")
    print(f"📦 Modules: {{len(project_data['modules'])}}")
    print(f"✅ Total tasks: {{len(todos)}}")
    
    high_priority = sum(1 for t in todos if t['priority'] == 'high')
    medium_priority = sum(1 for t in todos if t['priority'] == 'medium')
    low_priority = sum(1 for t in todos if t['priority'] == 'low')
    
    print(f"\\n📊 Priority breakdown:")
    print(f"   🔴 High: {{high_priority}}")
    print(f"   🟡 Medium: {{medium_priority}}")
    print(f"   🟢 Low: {{low_priority}}")
    
    # Show task list
    print("\\n📝 Task List:")
    for i, todo in enumerate(todos, 1):
        priority_icon = {{'high': '🔴', 'medium': '🟡', 'low': '🟢'}}[todo['priority']]
        print(f"{{i:3d}}. {{priority_icon}} {{todo['content']}}")
    
    print("\\n✨ Task list initialized! Use 'claude' to start development.")
    print("💡 Tip: Claude Code will use this task list to guide development.")


if __name__ == "__main__":
    main()
''',

            'claude_dev_resume': '''#!/usr/bin/env python3
"""Start or resume Claude Code development session with task context."""
import subprocess
import sys
from pathlib import Path


def check_claude_installed():
    """Check if Claude Code CLI is installed."""
    try:
        result = subprocess.run(
            ["claude", "--version"], 
            capture_output=True, 
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_project_context():
    """Get current project context for Claude."""
    context_parts = []
    
    # Check for CLAUDE.md
    if Path("CLAUDE.md").exists():
        context_parts.append("Please review CLAUDE.md for project requirements and scope.")
    
    # Check for TASKS.md
    if Path("TASKS.md").exists():
        context_parts.append("Check TASKS.md for the complete task list.")
    
    # Check for TODO.md files
    todo_files = list(Path(".").rglob("TODO.md"))
    if todo_files:
        context_parts.append(f"Found {{len(todo_files)}} TODO.md files tracking progress.")
    
    # Check for .claude directory
    if Path(".claude").exists():
        context_parts.append("Project has Claude Code configuration in .claude/")
    
    return " ".join(context_parts)


def create_startup_prompt():
    """Create an intelligent startup prompt for Claude."""
    context = get_project_context()
    
    prompt = f"""I'm ready to help with development. {{context}}

Let me start by:
1. Using TodoRead to check the current task list
2. Reviewing project structure and requirements
3. Identifying the next task to work on

What would you like me to focus on today?"""
    
    return prompt


def main():
    """Start Claude Code with project context."""
    if not check_claude_installed():
        print("❌ Claude Code CLI not found!")
        print("📦 Install it first: npm install -g @anthropic-ai/claude-code")
        print("📚 Documentation: https://github.com/anthropics/claude-code")
        sys.exit(1)
    
    print("🚀 Starting Claude Code development session...")
    print("📋 Loading project context...")
    
    # Get startup prompt
    prompt = create_startup_prompt()
    
    # Start Claude with the prompt
    try:
        # Use subprocess to start Claude with the prompt
        subprocess.run(["claude", prompt], check=False)
    except KeyboardInterrupt:
        print("\\n👋 Development session ended.")
    except Exception as e:
        print(f"❌ Error starting Claude: {{e}}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''
        }