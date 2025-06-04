# Claude Scaffold
![claude-scaffold](https://github.com/user-attachments/assets/01168397-4dff-40fc-92d9-274f1d1934c7)

A powerful Python project scaffolding tool that generates well-structured, self-documenting project skeletons with built-in best practices. Designed to enhance Claude Code capabilities by providing intelligent project templates that seamlessly integrate with AI-assisted development workflows.

## Purpose

Claude Scaffold enhances Claude Code's capabilities by providing:
- **Structured Project Templates**: Pre-configured projects optimized for AI-assisted development
- **Built-in Task Management**: Seamlessly integrates with Claude Code's task tracking system
- **Documentation-First Approach**: Ensures AI has complete context for better code generation
- **Enforced Best Practices**: Guides AI to follow TDD, clean architecture, and coding standards

## Features

- **Interactive Project Setup**: Guided project creation with intelligent suggestions
- **Multiple Project Types**: Web apps, CLIs, libraries, APIs, ML projects, and custom templates
- **Smart Module Generation**: Automatically creates module structure with documentation
- **Task Management**: Built-in task tracking and prioritization system
- **Best Practices**: Enforces TDD, documentation-first development, and clean architecture
- **Rich CLI Interface**: Beautiful terminal UI with progress tracking and status updates
- **Claude Code Integration**: Includes custom commands for seamless AI-assisted development

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/soheilshahi42/claude-scaffold.git
```

Or clone and install locally:

```bash
git clone https://github.com/soheilshahi42/claude-scaffold.git
cd claude-scaffold
pip install -e .
```

## Quick Start

Create a new project:

```bash
claude-scaffold new my-project
```

Add a task to an existing project:

```bash
claude-scaffold add-task . api "Create user authentication endpoints" --priority high
```

## Project Types

- **Web Application**: Full-stack or frontend web projects
- **Command Line Tool**: CLI applications and utilities
- **Python Library**: Reusable packages and modules
- **API Service**: REST or GraphQL API services
- **Machine Learning**: Data science and ML projects
- **Custom**: Define your own project structure

## Generated Project Structure

```
my-project/
├── src/              # Source code modules
├── tests/            # Test files (mirrors src structure)
├── docs/             # Project documentation
├── .claude/          # Claude Code integration
│   └── commands/     # Custom Claude Code commands
├── .github/          # GitHub workflows (optional)
└── setup.py          # Package configuration
```

## Claude Code Integration

Every generated project includes custom Claude Code commands that work with the `claude` CLI:

```bash
# Initialize task list from project configuration
claude init-tasks

# Start development session with full project context
claude dev
```

### Available Commands in Generated Projects

1. **`claude init-tasks`** - Reads your project's CLAUDE.md and TASKS.md files to create a structured TODO list
   - Parses all defined tasks with their priorities
   - Creates a task list compatible with Claude's TodoRead/TodoWrite tools
   - Shows task statistics and breakdown by priority

2. **`claude dev`** - Starts an AI-assisted development session
   - Loads complete project context (CLAUDE.md, TASKS.md, TODO.md)
   - Prompts Claude to check current tasks and continue development
   - Ensures Claude follows the defined project scope and constraints

These commands ensure Claude has complete understanding of your project structure, tasks, and constraints, making AI-assisted development more efficient and aligned with your project goals.

### Typical Workflow

```bash
# 1. Create a new project
claude-scaffold new my-awesome-project

# 2. Navigate to the project
cd my-awesome-project

# 3. Initialize the task list for Claude
claude init-tasks

# 4. Start development with Claude
claude dev
```

## Key Benefits

- **Consistent Structure**: Every project follows the same organizational patterns
- **Documentation-First**: Forces documentation before implementation
- **Test-Driven**: Encourages writing tests before code
- **Task Tracking**: Built-in task management system
- **Extensible**: Easy to customize for your team's needs

## Requirements

- Python 3.8 or higher
- Git (optional, for repository initialization)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.
