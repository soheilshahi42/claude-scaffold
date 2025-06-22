# Module Description Prompt

## Description

This prompt generates precise, concise descriptions for individual modules. It creates action-oriented descriptions that clearly state the module's primary responsibility within the project context.

## Purpose

- Generate clear, concise module descriptions
- Ensure consistent description format
- State primary responsibilities clearly
- Maintain context-specific relevance
- Follow character limits for readability

## Prompt Content

```
Generate a precise module description.

**MODULE:** {module_name}
**PROJECT TYPE:** {project_type}

**DESCRIPTION REQUIREMENTS:**
- Start with action verb (Manages, Handles, Provides, Implements, Orchestrates)
- State primary responsibility clearly
- Maximum 80 characters
- Be specific to {project_type} context

**EXAMPLES:**
- auth: "Manages user authentication, sessions, and JWT token generation"
- payment_processing: "Handles payment transactions, refunds, and webhook processing"
- data_pipeline: "Orchestrates ETL workflows and data transformation tasks"

**OUTPUT:**
Return ONLY the description text (no quotes, no formatting).
```