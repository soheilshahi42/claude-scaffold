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
'''
        }