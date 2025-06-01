#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from .scaffold import ClaudeScaffold
from .interactive.interactive import InteractiveSetup


def print_banner():
    """Print the Claude Scaffold banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ╔═╗╦  ╔═╗╦ ╦╔╦╗╔═╗  ╔═╗╔═╗╔═╗╔═╗╔═╗╔═╗╦  ╔╦╗           ║
║     ║  ║  ╠═╣║ ║ ║║║╣   ╚═╗║  ╠═╣╠╣ ╠╣ ║ ║║   ║║           ║
║     ╚═╝╩═╝╩ ╩╚═╝═╩╝╚═╝  ╚═╝╚═╝╩ ╩╚  ╚  ╚═╝╩═╝═╩╝           ║
║                                                               ║
║     Generate self-documenting Claude Code project skeletons   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    parser = argparse.ArgumentParser(
        description="Claude Scaffold - Generate self-documenting Claude code project skeletons",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  new         Create a new Claude-ready project with comprehensive setup
  add-task    Add a task to an existing Claude Scaffold project
  
Examples:
  claude-scaffold new my_project                        # Interactive project creation
  claude-scaffold new my_project --no-interactive      # Create with minimal defaults
  claude-scaffold new my_project --force               # Overwrite existing project
  claude-scaffold add-task . api "Create user endpoints" --priority high
  
Project Types:
  • Web Application     - Full-stack or frontend web projects
  • CLI Tool           - Command-line applications
  • Python Library     - Reusable packages
  • API Service        - REST/GraphQL APIs
  • ML Project         - Machine learning projects
  • Custom             - Define your own structure
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # New project command
    new_parser = subparsers.add_parser(
        'new',
        help='Create a new Claude-ready project',
        description='Create a new project with Claude Scaffold\'s comprehensive structure'
    )
    new_parser.add_argument(
        'project_name',
        help='Name of the project to create'
    )
    new_parser.add_argument(
        '--path',
        type=Path,
        help='Custom path where to create the project (default: current directory)'
    )
    new_parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing project without confirmation'
    )
    new_parser.add_argument(
        '--no-interactive',
        action='store_true',
        help='Skip interactive setup and use minimal defaults'
    )
    
    # Add task command
    add_task_parser = subparsers.add_parser(
        'add-task',
        help='Add a task to an existing project',
        description='Add a new task to a Claude Scaffold project with automatic documentation'
    )
    add_task_parser.add_argument(
        'project_path',
        type=Path,
        help='Path to the Claude Scaffold project (use . for current directory)'
    )
    add_task_parser.add_argument(
        'module',
        help='Module name to add the task to'
    )
    add_task_parser.add_argument(
        'task_title',
        help='Title of the task (use quotes for multi-word titles)'
    )
    add_task_parser.add_argument(
        '--priority',
        choices=['high', 'medium', 'low'],
        default='medium',
        help='Task priority level (default: medium)'
    )
    
    args = parser.parse_args()
    
    # Show banner for interactive commands
    if args.command == 'new' and not args.no_interactive:
        print_banner()
    
    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(1)
    
    try:
        scaffold = ClaudeScaffold()
        
        if args.command == 'new':
            success = scaffold.create_project(
                project_name=args.project_name,
                project_path=args.path,
                force=args.force,
                interactive=not args.no_interactive
            )
            sys.exit(0 if success else 1)
        
        elif args.command == 'add-task':
            # Resolve project path
            project_path = args.project_path.resolve()
            
            success = scaffold.add_task(
                project_path=project_path,
                module_name=args.module,
                task_title=args.task_title,
                priority=args.priority
            )
            sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()