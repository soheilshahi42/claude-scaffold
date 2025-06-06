"""Command templates for Claude Scaffold projects."""

from typing import Dict


class CommandTemplates:
    """Templates for custom Claude commands."""

    @staticmethod
    def get_templates() -> Dict[str, str]:
        """Return all command templates."""
        return {
            "init-tasks.md": """Initialize and review the task list for this project.

First, read through CLAUDE.md to understand the project structure and all defined modules.

Then, read TASKS.md to see all project tasks with their priorities and module assignments.

Finally, use the TodoWrite tool to create a comprehensive task list that includes:
1. A setup task to review project requirements
2. All tasks from TASKS.md organized by module
3. Module setup tasks for each defined module
4. A final integration testing task

After creating the task list, provide a summary showing:
- Total number of tasks
- Breakdown by priority (high/medium/low)
- Current project status
- Suggested next steps based on priority

This will prepare the project for systematic development following the defined structure.
""",
            "dev.md": """Start or resume development on this project by following these steps:

1. First, use TodoRead to check the current task list and see what needs to be done
2. Read CLAUDE.md to understand the project structure, modules, and constraints
3. Read GLOBAL_RULES.md to understand the immutable project rules
4. Identify the highest priority pending task from the todo list
5. For the selected task:
   - Find the module it belongs to
   - Read the module's CLAUDE.md file for specific implementation details
   - Check if there's existing research in docs/ for this task
   - Follow the TDD workflow: write tests first, then implement
6. After completing a task, use TodoWrite to update its status
7. Provide a brief summary of what was accomplished and what should be done next

Remember: You must ONLY work on tasks that are defined in TASKS.md and ONLY create code in the modules specified in CLAUDE.md. Do not add new features or modules beyond what has been defined.

$ARGUMENTS
""",
            "test.md": """Run the project test suite and analyze the results.

Execute the following test command:
```bash
{test_command}
```

After running tests:
1. Analyze any failures or errors
2. Check test coverage percentages
3. Identify untested code paths
4. Suggest specific tests that should be added
5. If all tests pass, confirm the code quality

Provide a clear summary of the test results and any recommended actions.
""",
            "status.md": """Provide a comprehensive project status report.

1. Use TodoRead to get the current task list
2. Analyze task completion status:
   - Count completed vs pending tasks
   - Calculate completion percentage
   - Identify blocked or stalled tasks
3. Review recent git commits to understand recent progress
4. Check each module's implementation status
5. Identify any integration points that need attention

Create a status report that includes:
- Overall project completion percentage
- Module-by-module progress
- High-priority items that need immediate attention
- Potential risks or blockers
- Recommended next actions

$ARGUMENTS
""",
            "review.md": """Review code changes for quality and compliance with project standards.

$ARGUMENTS

Perform a comprehensive code review:
1. Check if changes align with module boundaries defined in CLAUDE.md
2. Verify adherence to GLOBAL_RULES.md
3. Ensure proper test coverage for new code
4. Validate documentation updates
5. Check for security issues or performance concerns
6. Verify code follows the project's style guide

Provide feedback on:
- Code quality and maintainability
- Test coverage and quality
- Documentation completeness
- Compliance with project rules
- Suggestions for improvement
""",
            "research.md": """Research and document approach for implementing a specific task or feature.

$ARGUMENTS

1. Identify the task/feature to research
2. Review existing project code and patterns
3. Research best practices and design patterns
4. Consider project constraints from GLOBAL_RULES.md
5. Document findings in docs/ directory
6. Create implementation plan following TDD approach

Deliverables:
- Research summary with references
- Proposed implementation approach
- Test strategy
- Potential risks and mitigations
- Integration considerations
""",
        }
