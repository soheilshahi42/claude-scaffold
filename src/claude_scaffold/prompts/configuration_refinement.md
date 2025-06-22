# Configuration Refinement Prompt

## Description

This prompt refines project configurations based on user feedback. It analyzes refinement requests and provides specific, actionable improvements to modules, tasks, rules, and other configuration aspects while maintaining consistency.

## Purpose

- Refine configurations based on user feedback
- Provide specific, actionable improvements
- Maintain configuration consistency
- Address scope, detail, and technical adjustments
- Track changes with clear reasoning

## Prompt Content

```
You are refining a project configuration based on user feedback.

**USER REQUEST:**
"{refinement_request}"

**CURRENT CONFIGURATION:**
- Project Name: {project_name}
- Project Type: {project_type}
- Modules Defined: {modules}
- Tasks Count: {tasks_count} tasks

**YOUR TASK:**
Analyze the user's feedback and provide specific, actionable improvements to the configuration.

**REFINEMENT APPROACH:**

1. **Understand the Request**
   - What specific aspect needs improvement?
   - Is it about scope, detail, organization, or accuracy?
   - Are there missing components?

2. **Types of Refinements**
   - **Scope Changes**: Add/remove modules or features
   - **Detail Enhancement**: More specific descriptions or requirements
   - **Technical Adjustments**: Different tech choices or approaches
   - **Task Modifications**: Break down, combine, or reorder tasks
   - **Rule Updates**: Adjust coding standards or practices

3. **Response Structure**
   Provide updates for relevant sections:
   - modules: Added/modified module definitions
   - tasks: New or updated task specifications
   - rules: Updated coding standards
   - architecture: Structural changes
   - metadata: Project description updates

**OUTPUT FORMAT:**
{
    "refinement_summary": "Brief description of changes made",
    "modules": {
        "added": [{"name": "...", "description": "...", "reason": "Why added"}],
        "modified": [{"name": "...", "changes": "What changed", "reason": "Why"}],
        "removed": [{"name": "...", "reason": "Why removed"}]
    },
    "tasks": {
        "added": [{"name": "...", "module": "...", "description": "..."}],
        "modified": [{"name": "...", "changes": "..."}],
        "removed": [{"name": "...", "reason": "..."}]
    },
    "rules": {
        "added": ["New rule 1", "New rule 2"],
        "modified": [{"old": "...", "new": "...", "reason": "..."}],
        "removed": ["Rule to remove"]
    },
    "other_changes": {
        "description": "Updated project description if needed",
        "architecture": "Architectural adjustments",
        "constraints": "New technical constraints"
    }
}

**REFINEMENT PRINCIPLES:**
- Address the specific concern raised
- Maintain consistency with existing configuration
- Provide clear reasoning for changes
- Keep changes focused and relevant
- Ensure technical feasibility

**COMMON REFINEMENT PATTERNS:**
- "Too generic" → Add specific implementation details
- "Missing X" → Add the missing component with full spec
- "Should use Y instead" → Replace with justification
- "Break down further" → Split into smaller, clearer pieces
- "Combine these" → Merge with clear new structure
```