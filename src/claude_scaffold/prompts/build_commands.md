# Build Commands Prompt

## Description

This prompt generates standard build commands for projects based on their technology stack. It provides production-ready commands for installation, testing, building, development, linting, formatting, cleaning, and validation.

## Purpose

- Generate appropriate build commands for the tech stack
- Ensure production-ready command configurations
- Include all essential development workflow commands
- Follow language-specific conventions
- Support CI/CD pipeline integration

## Prompt Content

```
You are a DevOps engineer setting up standard build commands for a project.

**PROJECT DETAILS:**
- Type: {project_type}
- Language: {language}

**REQUIRED COMMANDS:**
Provide the most appropriate, production-ready commands for this tech stack.

**COMMAND CATEGORIES:**

1. **install** - Install all dependencies
   - Include dev dependencies
   - Handle git hooks if applicable
   - Consider lock files

2. **test** - Run test suite
   - Include coverage reporting
   - Run in CI-friendly mode
   - Fail on coverage threshold if applicable

3. **build** - Production build
   - Optimize for production
   - Include type checking if applicable
   - Generate source maps

4. **dev** - Development server
   - Hot reload enabled
   - Debug mode
   - Source maps

5. **lint** - Code quality checks
   - Style checking
   - Static analysis
   - Type checking if applicable

6. **format** - Auto-format code
   - Apply project style
   - Fix auto-fixable issues

7. **clean** - Clean build artifacts
   - Remove dist/build folders
   - Clear cache

8. **validate** - Pre-commit validation
   - Run lint + test
   - Type check
   - Build check

**LANGUAGE-SPECIFIC EXAMPLES:**

For Node.js/TypeScript:
{
    "install": "npm ci && husky install",
    "test": "jest --coverage --ci",
    "build": "tsc && webpack --mode production",
    "dev": "nodemon --watch src --exec ts-node src/index.ts",
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --write \"src/**/*.{ts,tsx}\"",
    "clean": "rm -rf dist coverage",
    "validate": "npm run lint && npm run test && npm run build"
}

For Python:
{
    "install": "pip install -r requirements.txt -r requirements-dev.txt",
    "test": "pytest --cov=src --cov-report=html --cov-report=term",
    "build": "python -m build",
    "dev": "uvicorn main:app --reload --host 0.0.0.0 --port 8000",
    "lint": "flake8 src tests && mypy src",
    "format": "black src tests && isort src tests",
    "clean": "find . -type d -name __pycache__ -exec rm -rf {} + && rm -rf dist build *.egg-info",
    "validate": "make lint && make test"
}

**OUTPUT FORMAT:**
{
    "install": "Complete command with all flags",
    "test": "Test command with coverage and CI flags",
    "build": "Production build command",
    "dev": "Development server command",
    "lint": "Linting command with all checks",
    "format": "Auto-formatting command",
    "clean": "Cleanup command",
    "validate": "Pre-commit validation command",
    "docker:build": "Docker build command if applicable",
    "docker:run": "Docker run command if applicable"
}

**CONSIDERATIONS FOR {project_type} in {language}:**
- Use the most common build tools for {language}
- Include {project_type}-specific optimizations
- Ensure commands work across different OS platforms
- Prefer lock files for reproducible builds
- Include helpful flags for debugging
```