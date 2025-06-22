# Task Details Batch Prompt

## Description

This prompt generates detailed implementation plans for multiple tasks at once. It creates comprehensive plans including implementation approach, subtasks following TDD methodology, acceptance criteria, and dependencies for each task.

## Purpose

- Generate implementation details for multiple tasks efficiently
- Ensure consistent TDD approach across all tasks
- Define clear subtasks and acceptance criteria
- Identify dependencies between tasks
- Maintain project-specific context

## Prompt Content

```
You are a technical lead creating implementation plans for multiple development tasks.

**PROJECT CONTEXT:**
- Type: {project_type}
- Language: {language}

**TASKS TO DETAIL:**
{tasks_json}

**FOR EACH TASK, PROVIDE:**

1. **Implementation Approach** (approach):
   - 2-3 sentences describing HOW to build this
   - Mention specific patterns, libraries, or techniques
   - Be concrete, not abstract

2. **Subtasks** (subtasks) - 4-6 items following TDD:
   - Start with "Test:" tasks (minimum 2)
   - Follow with "Implement:" tasks
   - End with "Refactor:" or "Document:" if needed
   - Each subtask should be 1-day or less of work

3. **Acceptance Criteria** (acceptance_criteria) - 3-4 specific items:
   - User-visible behavior or technical requirements
   - Measurable and testable
   - Include edge cases

4. **Dependencies** (dependencies):
   - Other tasks that must complete first
   - External services or libraries needed
   - Knowledge prerequisites

**SUBTASK EXAMPLES:**

GOOD:
- "Test: Write unit tests for email validation with edge cases"
- "Test: Create integration tests for login flow with 2FA"
- "Implement: Build UserRepository with CRUD operations"
- "Implement: Create JWT token generation and validation"
- "Refactor: Extract validation logic to reusable middleware"

BAD:
- "Test: Write tests" (too vague)
- "Implement: Build the feature" (not specific)
- "Test: Test everything" (not actionable)

**OUTPUT FORMAT:**
{
    "task_name": {
        "approach": "Clear implementation strategy referencing specific tools/patterns",
        "subtasks": [
            "Test: Specific test scenario",
            "Test: Another test scenario",
            "Implement: Specific component/feature",
            "Implement: Another component",
            "Refactor: Specific improvement"
        ],
        "acceptance_criteria": [
            "Specific user-facing requirement",
            "Technical requirement with metric",
            "Edge case handling"
        ],
        "dependencies": [
            "prerequisite_task_name",
            "required_library_or_service"
        ]
    },
    "next_task": { ... }
}

**TASK COMPLEXITY GUIDELINES:**
- Simple tasks (CRUD, basic UI): 3-4 subtasks
- Medium tasks (auth, integrations): 4-5 subtasks
- Complex tasks (architecture, algorithms): 5-6 subtasks

**{language} SPECIFIC CONSIDERATIONS:**
- Use {language} idioms and best practices
- Reference common {language} testing frameworks
- Suggest {language}-specific libraries where appropriate

**{project_type} SPECIFIC PATTERNS:**
- Follow standard {project_type} architecture patterns
- Include {project_type}-specific testing needs
- Consider {project_type} security/performance requirements
```