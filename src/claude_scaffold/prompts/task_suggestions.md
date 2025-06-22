# Task Suggestions Prompt

## Description

This prompt creates comprehensive task lists for new projects, covering the entire project lifecycle from setup to deployment. It generates 12-18 specific, actionable development tasks organized by category and ordered by dependencies.

## Purpose

- Generate complete project task lists
- Ensure comprehensive coverage of project needs
- Order tasks by logical dependencies
- Include all lifecycle phases
- Maintain project-specific relevance

## Prompt Content

```
You are a technical project manager creating a comprehensive task list for a new project.

**PROJECT CONTEXT:**
- Type: {project_type}
- Language: {language}
- Description: {description}
- Modules: {modules}

**YOUR TASK:**
Create 12-18 specific, actionable development tasks that cover the entire project lifecycle.

**TASK CATEGORIES TO INCLUDE:**

1. **Setup & Configuration** (2-3 tasks)
   - Project initialization
   - Development environment
   - CI/CD pipeline

2. **Core Infrastructure** (3-4 tasks)
   - Database setup
   - Authentication system
   - API structure
   - Error handling

3. **Feature Implementation** (4-6 tasks)
   - Core business logic
   - User-facing features
   - Integration points

4. **Quality Assurance** (2-3 tasks)
   - Unit test suite
   - Integration tests
   - Performance testing

5. **Deployment & Operations** (2-3 tasks)
   - Production setup
   - Monitoring/logging
   - Documentation

**TASK NAMING PRINCIPLES:**
- Start with action verb: Create, Implement, Setup, Configure, Add, Build
- Be specific about what's being built
- Include the target component/module
- Keep under 50 characters

**GOOD TASK EXAMPLES:**
✓ "Setup PostgreSQL database with migrations"
✓ "Implement JWT authentication middleware"
✓ "Create user registration API endpoint"
✓ "Add comprehensive error handling system"
✓ "Configure GitHub Actions CI/CD pipeline"

**BAD TASK EXAMPLES:**
✗ "Do authentication" (too vague)
✗ "Write code for the user module" (not specific)
✗ "Setup everything" (too broad)
✗ "Implement all API endpoints" (too large)

**TASK ORDERING PRINCIPLES:**
1. Dependencies first (database before models)
2. Infrastructure before features
3. Core features before nice-to-haves
4. Testing alongside implementation
5. Deployment preparation near the end

**{language} SPECIFIC TASKS:**
- Include {language}-specific setup tasks
- Use {language} tooling conventions
- Consider {language} testing frameworks

**{project_type} SPECIFIC FOCUS:**
- Emphasize tasks critical to {project_type}
- Include {project_type} best practices
- Address {project_type} common requirements

**OUTPUT FORMAT:**
Return a JSON array of 12-18 task names in logical order:

["First task", "Second task", ...]

**EXAMPLE OUTPUT for E-commerce API:**
[
    "Initialize Node.js project with TypeScript",
    "Setup PostgreSQL database with Docker",
    "Create database migration system",
    "Implement user authentication with JWT",
    "Create product catalog data models",
    "Build product search API endpoints",
    "Implement shopping cart functionality",
    "Add payment processing with Stripe",
    "Create order management system",
    "Implement email notifications",
    "Add comprehensive error handling",
    "Setup unit test framework with Jest",
    "Write API integration tests",
    "Configure rate limiting and security",
    "Setup production deployment pipeline",
    "Add application monitoring with Sentry",
    "Create API documentation with Swagger"
]
```