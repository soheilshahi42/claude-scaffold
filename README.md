# Claude Scaffold
![claude-scaffold](https://github.com/user-attachments/assets/01168397-4dff-40fc-92d9-274f1d1934c7)

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/soheilshahi42/claude-scaffold/actions/workflows/tests.yml/badge.svg)](https://github.com/soheilshahi42/claude-scaffold/actions/workflows/tests.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub stars](https://img.shields.io/github/stars/soheilshahi42/claude-scaffold?style=social)](https://github.com/soheilshahi42/claude-scaffold)
[![GitHub issues](https://img.shields.io/github/issues/soheilshahi42/claude-scaffold)](https://github.com/soheilshahi42/claude-scaffold/issues)

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

## Configuration Files

For complex projects, you can define the entire project structure in a YAML configuration file:

```yaml
# claude-scaffold.yaml
project_name: my-app
project_type: web
description: A full-stack web application
modules:
  - name: frontend
    description: React frontend application
  - name: backend
    description: FastAPI backend service
  - name: database
    description: Database models and migrations
  - name: auth
    description: Authentication and authorization
tasks:
  - title: Set up user authentication
    module: auth
    priority: high
  - title: Create database schema
    module: database
    priority: high
  - title: Design API endpoints
    module: backend
    priority: medium
  - title: Build login UI
    module: frontend
    priority: medium
rules:
  suggested:
    - Follow REST API conventions
    - Use TypeScript for type safety
    - Write unit tests for all endpoints
  custom:
    - All API endpoints must have OpenAPI documentation
    - Use JWT tokens for authentication
constraints:
  - Python 3.10+
  - Node.js 18+
  - PostgreSQL 14+
```

Create a project using the configuration file:

```bash
claude-scaffold new my-app --config claude-scaffold.yaml --no-interactive
```

This is especially useful for:
- Team templates and standards
- Reproducing project structures
- CI/CD automation
- Sharing project blueprints

## Claude Code Integration

Every generated project is optimized for use with Claude Code and includes custom slash commands in the `.claude/commands/` directory.

### Custom Slash Commands

Generated projects include the following slash commands that you can use within Claude Code:

- **`/project:init-tasks`** - Initialize task tracking from your project configuration
  - Reads CLAUDE.md and TASKS.md to understand project structure
  - Creates a comprehensive task list using TodoWrite
  - Shows task statistics and priority breakdown
  
- **`/project:dev`** - Start or resume development on the project
  - Checks current tasks with TodoRead
  - Loads project context and constraints
  - Guides development following TDD workflow
  
- **`/project:test`** - Run project tests and analyze results
  - Executes the test suite
  - Analyzes coverage and failures
  - Suggests improvements
  
- **`/project:status`** - Get comprehensive project status
  - Shows task completion progress
  - Reviews recent changes
  - Identifies blockers and next actions
  
- **`/project:review`** - Review code changes
  - Checks compliance with project rules
  - Validates test coverage
  - Provides improvement suggestions
  
- **`/project:research`** - Research implementation approaches
  - Documents findings in docs/ directory
  - Creates implementation plans
  - Follows TDD methodology

### Working with Claude Code

After creating a project with claude-scaffold:

```bash
# 1. Create a new project
claude-scaffold new my-awesome-project

# 2. Navigate to the project
cd my-awesome-project

# 3. Start Claude Code
claude

# 4. Use the custom commands:
claude> /project:init-tasks
claude> /project:dev
claude> /project:status
```

The generated project structure and custom commands ensure Claude has complete understanding of your project's modules, tasks, and constraints, making AI-assisted development more focused and efficient.

## Key Benefits

- **Consistent Structure**: Every project follows the same organizational patterns
- **Documentation-First**: Forces documentation before implementation
- **Test-Driven**: Encourages writing tests before code
- **Task Tracking**: Built-in task management system
- **Extensible**: Easy to customize for your team's needs

## Requirements

- Python 3.10 or higher
- Git (optional, for repository initialization)
- Claude Code CLI (required for using custom commands)
  - Install with: `npm install -g @anthropic-ai/claude-cli`
  - Documentation: https://github.com/anthropics/claude-code

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.
