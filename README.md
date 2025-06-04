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

```bash
pip install claude-scaffold
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

Every generated project includes custom Claude Code commands:

```bash
# Initialize task list from project configuration
claude-code init-tasks

# Start development session with full project context
claude-code dev
```

These commands ensure Claude Code has complete understanding of your project structure, tasks, and constraints.

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
