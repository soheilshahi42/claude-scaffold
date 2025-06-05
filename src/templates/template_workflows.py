"""Workflow templates for Claude Scaffold projects."""

from typing import Dict


class WorkflowTemplates:
    """Templates for various workflow documents."""

    @staticmethod
    def get_templates() -> Dict[str, str]:
        """Return all workflow templates."""
        return {
            "research_template": """# Research: {task_name}

## Objective
{research_objective}

## Key Questions
{key_questions}

## Research Findings

### Requirements Analysis
{findings}

### Technical Approach
_To be completed during research_

### Prior Art / References
{references}

## Recommendations
{recommendations}

## Implementation Plan
{next_steps}

## Open Questions
_List any unresolved questions or concerns_

## Decision Log
- **Date**: _Today's date_
- **Decision**: _Key decisions made_
- **Rationale**: _Why this approach was chosen_

---
Research completed by: _Your name_
Date: _Completion date_
""",
            "tdd_template": """# Test-Driven Development Plan: {task_name}

## Test Categories

### Unit Tests
- [ ] Test case 1: _Description_
- [ ] Test case 2: _Description_
- [ ] Test case 3: _Description_

### Integration Tests
- [ ] Test case 1: _Description_
- [ ] Test case 2: _Description_

### Edge Cases
- [ ] Null/empty inputs
- [ ] Boundary conditions
- [ ] Error scenarios

## Test Implementation Order
1. Write simplest failing test
2. Implement minimum code to pass
3. Refactor if needed
4. Repeat for next test

## Acceptance Criteria
_Define what "done" looks like_

## Performance Benchmarks
_If applicable, define performance requirements_
""",
            "implementation_checklist": """# Implementation Checklist: {task_name}

## Pre-Implementation
- [ ] Research completed and documented
- [ ] Approach reviewed and approved
- [ ] Dependencies identified
- [ ] Tests written (TDD)

## Implementation
- [ ] Core functionality implemented
- [ ] Error handling added
- [ ] Logging/monitoring added
- [ ] Performance optimized
- [ ] Security considerations addressed

## Post-Implementation
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Integration tested
- [ ] Performance validated

## Deployment Readiness
- [ ] Migration plan (if needed)
- [ ] Rollback plan documented
- [ ] Monitoring configured
- [ ] Team notified

---
Completed by: _Your name_
Date: _Completion date_
""",
        }
