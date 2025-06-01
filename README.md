# Claude Scaffold

A powerful command-line scaffolding tool that generates complete, self-documenting Claude Code project skeletons in seconds, fully wired for iterative task execution and TDD. Now with **AI-powered project configuration** using Claude in headless mode!

## ✨ Features

### 🎯 Comprehensive Project Setup
- **Interactive Q&A System**: Guides you through project configuration with intelligent questions
- **Multiple Project Types**: Web apps, CLI tools, libraries, APIs, ML projects, or custom
- **Smart Defaults**: Suggests modules, tasks, and conventions based on project type
- **Review & Confirm**: Preview your configuration before creation

### 📚 Self-Documenting Structure
- **CLAUDE.md in Every Folder**: Explains folder role, conventions, and usage
- **GLOBAL_RULES.md**: Immutable project standards enforced across all code
- **Module Documentation**: Detailed specs, tasks, and local conventions
- **Research Templates**: Pre-structured docs for task investigation

### 🔄 Task Management System
- **Global Task List**: Title-only list with module references
- **Module Task Details**: Complete specifications in module CLAUDE.md
- **Progress Tracking**: TODO.md files with automatic checkboxes
- **TDD Workflow**: Enforced research → test → implement → verify order

### 🤖 Claude Code Integration
- **AI-Powered Setup**: Claude enhances your configuration with intelligent suggestions
- **Smart Documentation**: AI-generated module docs, task specs, and research topics
- **Intelligent Task Breakdown**: Claude creates logical subtasks following TDD principles
- **Custom Commands**: Auto-generated test and build commands
- **Settings Configuration**: Optimized .claude/settings.json
- **Memory Hierarchy**: Project, module, and local CLAUDE.md files
- **Workflow Templates**: TDD, research, and implementation guides

## 📦 Installation

```bash
# Install from PyPI (coming soon)
pip install claude-scaffold

# Install from source
git clone https://github.com/yourusername/claude-scaffold.git
cd claude-scaffold
pip install -e .
```

### Requirements
- Python 3.7+
- questionary (for interactive prompts)
- colorama (for colored output)
- pyyaml (for configuration)

## 🚀 Quick Start

### Create a New Project

```bash
# Interactive mode with Claude AI enhancement - recommended!
claude-scaffold new my_project

# The tool will:
# 1. Check for Claude CLI availability
# 2. Guide you through project configuration
# 3. Ask if you want Claude to enhance your setup
# 4. Use AI to generate intelligent documentation
# 5. Continue refining until configuration is perfect
# 6. Create a fully documented project structure
```

### What Claude Adds

When Claude is available, you'll see:
```
✅ Claude CLI detected - intelligent configuration available!

🤖 Would you like Claude to enhance your configuration with intelligent suggestions? (Yes)

🤖 Consulting Claude for intelligent project configuration...
📝 Generating detailed task specifications...
📚 Enhancing module documentation...
📏 Generating comprehensive project rules...
✅ Validating project configuration...
```

### Non-Interactive Mode

```bash
# Create with minimal defaults
claude-scaffold new my_project --no-interactive

# Force overwrite existing project
claude-scaffold new my_project --force
```

### Add Tasks to Existing Project

```bash
# Add a task with priority
claude-scaffold add-task . api "Create user authentication" --priority high
```

## 📁 Generated Project Structure

```
my_project/
│
├── .claude/                 # Claude Code configuration
│   ├── settings.json       # Tool permissions and context
│   ├── commands/           # Custom commands
│   └── project_config.yaml # Project configuration
│
├── GLOBAL_RULES.md         # Immutable project standards
├── TASKS.md               # Global task list (titles only)
├── TODO.md                # Root-level progress tracker
├── CLAUDE.md              # Root documentation
│
├── [module_name]/         # Generated for each module
│   ├── __init__.py       # Module initialization
│   ├── CLAUDE.md         # Module docs + task details
│   ├── TODO.md           # Module task checklist
│   └── docs/             # Task research files
│       └── [task].md     # Research template
│
└── tests/                 # Test structure
    └── [module_name]/    # Module tests
        └── test_*.py     # Test files with TDD stubs
```

## 🎨 Project Types

### Web Application
- Suggested modules: frontend, backend, api, database, auth
- Includes: static/, templates/ directories
- Testing: jest/pytest setup

### CLI Tool
- Suggested modules: commands, utils, config, output
- Focus on: POSIX conventions, help docs
- Testing: pytest with CLI testing

### Python Library
- Suggested modules: core, utils, exceptions, types
- Focus on: Clean API, type hints
- Testing: High coverage targets

### API Service
- Suggested modules: routes, models, services, middleware
- Includes: OpenAPI/Swagger setup
- Testing: Integration tests

### ML Project
- Suggested modules: data, models, training, evaluation
- Includes: notebooks/, data/, models/
- Testing: Experiment tracking

## 🔧 Configuration

### Interactive Setup Flow

1. **Project Type**: Choose from predefined types or custom
2. **Description**: Provide project overview
3. **Style Guide**: PEP8, Black, Google, or custom
4. **Modules**: Accept suggestions or define your own
5. **Tasks**: Create initial task list with priorities
6. **Rules**: Select from suggestions or add custom rules
7. **Constraints**: Define technical requirements
8. **Commands**: Set up build, test, and dev commands
9. **Claude Enhancement** (if available):
   - AI analyzes your configuration
   - Generates detailed documentation
   - Creates comprehensive task breakdowns
   - Suggests architecture patterns
   - Validates and refines until perfect
10. **Review**: Confirm or modify configuration

### Claude Enhancement Loop

When Claude is available, the tool enters an enhancement loop:

```
🎯 Is this configuration perfect? (yes/no/modify):
```

- **yes**: Creates the project with all enhancements
- **no**: Tell Claude what needs improvement
- **modify**: Make specific changes to the configuration

Claude will continue refining based on your feedback until you're satisfied.

### Configuration Storage

Project configuration is saved in `.claude/project_config.yaml` for:
- Adding tasks later
- Regenerating documentation
- Team sharing and consistency

## 📋 Task Management Workflow

### 1. Global Task List (TASKS.md)
```markdown
- Implement user authentication ← details in /auth/CLAUDE.md
- Create REST API endpoints ← details in /api/CLAUDE.md
```

### 2. Module Task Details ([module]/CLAUDE.md)
```markdown
### Task 1 – Implement user authentication
**Priority**: high
**Goal**: Build secure login system
**Research file**: docs/implement_user_authentication.md
**Sub-tasks**: see TODO.md
```

### 3. Progress Tracking ([module]/TODO.md)
```markdown
- [ ] Research: Implement user authentication
- [ ] Document findings for: Implement user authentication
- [ ] Write failing tests for: Implement user authentication
- [ ] Implement: Implement user authentication
- [ ] Verify all tests pass for: Implement user authentication
- [ ] Update documentation for: Implement user authentication
```

## 🤝 Claude Code Integration

### Custom Commands

The tool generates custom commands in `.claude/commands/`:
- `test.py` - Run all tests with coverage
- `build.py` - Execute build pipeline

### Settings Configuration

Optimized `.claude/settings.json` includes:
- Tool permissions
- Context patterns
- Workflow definitions

### Memory Hierarchy

1. **Project Memory** (`./CLAUDE.md`)
   - Team-shared instructions
   - Global conventions

2. **Module Memory** (`./[module]/CLAUDE.md`)
   - Module-specific rules
   - Local patterns

3. **Personal Memory** (`./CLAUDE.local.md`)
   - Developer notes (git-ignored)

## 🎯 Best Practices

### For Claude Code Users

1. **Start with Research**: Use research templates before implementing
2. **Follow TDD**: Write tests first, always
3. **Update Progress**: Check off TODO items as completed
4. **Maintain Docs**: Keep CLAUDE.md files current

### For Project Setup

1. **Be Specific**: Detailed task titles help Claude understand intent
2. **Modular Design**: Keep modules focused and cohesive
3. **Clear Rules**: Explicit rules prevent ambiguity
4. **Iterative Approach**: Start simple, add complexity gradually

## 🛠️ Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_scaffold.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built specifically for [Claude Code](https://github.com/anthropics/claude-code) by Anthropic, leveraging best practices from:
- Modern CLI design patterns
- Test-Driven Development methodology
- Self-documenting code principles
- Claude's context-aware capabilities

---

**Note**: This tool enforces strict TDD and documentation practices. All generated projects follow the research → test → implement → verify workflow to ensure high-quality, maintainable code.