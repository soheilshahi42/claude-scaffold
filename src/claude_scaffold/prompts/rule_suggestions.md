# Rule Suggestions Prompt

## Description

This prompt establishes comprehensive coding standards and best practices for development teams. It generates 12-15 specific, enforceable rules covering code style, architecture, error handling, security, testing, performance, documentation, and development workflow.

## Purpose

- Create comprehensive coding standards
- Ensure code quality and consistency
- Establish enforceable best practices
- Cover all aspects of development
- Maintain language and project-specific relevance

## Prompt Content

```
You are establishing coding standards and best practices for a development team.

**PROJECT CONTEXT:**
- Type: {project_type}
- Language: {language}  
- Description: {description}

**YOUR TASK:**
Create 12-15 specific, enforceable coding rules that ensure quality, consistency, and maintainability.

**RULE CATEGORIES:**

1. **Code Style & Formatting** (2 rules)
   - Naming conventions
   - File organization
   - Import/dependency management

2. **Architecture & Design** (2-3 rules)
   - Design patterns to follow
   - Module boundaries
   - Dependency principles

3. **Error Handling** (2 rules)
   - Exception management
   - Logging practices
   - User feedback

4. **Security** (2 rules)
   - Input validation
   - Authentication/authorization
   - Sensitive data handling

5. **Testing** (2 rules)
   - Coverage requirements
   - Test organization
   - Mock usage

6. **Performance** (1-2 rules)
   - Optimization requirements
   - Resource management
   - Scalability considerations

7. **Documentation** (2 rules)
   - Code documentation
   - API documentation
   - Commit messages

8. **Development Workflow** (1-2 rules)
   - Version control
   - Code review
   - Deployment practices

**RULE CHARACTERISTICS:**
✓ **Specific**: "Functions must be <50 lines" not "Keep functions small"
✓ **Measurable**: Can be verified objectively
✓ **Actionable**: Developer knows what to do
✓ **Justified**: Clear benefit to the project
✓ **Enforceable**: Can be checked (manually or automated)

**{language} SPECIFIC EXAMPLES:**

For Python:
- "Use type hints for all function parameters and return values"
- "Follow PEP 8 with 88-character line limit (Black formatter)"
- "Use dataclasses for data models instead of dictionaries"

For JavaScript/TypeScript:
- "Use strict TypeScript with no 'any' types except in documented edge cases"
- "Prefer functional components with hooks over class components"
- "All async functions must have proper error handling with try-catch"

For Java:
- "Use immutable objects for DTOs and value objects"
- "Follow single responsibility principle: max 1 public method per class"
- "Use constructor injection for all dependencies"

**{project_type} SPECIFIC CONSIDERATIONS:**

For APIs:
- "All endpoints must validate input against JSON schema"
- "API responses must include consistent error format"
- "Use pagination for any endpoint returning collections"

For Web Apps:
- "Components must be accessible (WCAG 2.1 AA compliant)"
- "Implement progressive enhancement for JavaScript features"
- "Cache static assets with versioned filenames"

**OUTPUT FORMAT:**
Return a JSON array of 12-15 specific rule strings:

[
    "Specific, enforceable rule 1",
    "Specific, enforceable rule 2",
    ...
]

**AVOID:**
- Vague rules like "Write clean code"
- Overly restrictive rules that hinder productivity
- Rules that conflict with {language} idioms
- Generic rules that apply to any project
```