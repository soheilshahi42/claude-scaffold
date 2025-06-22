Determine the most appropriate module for a task.

**TASK:** {task}
**AVAILABLE MODULES:** {modules}

**ASSIGNMENT PRINCIPLES:**
1. Match task domain to module responsibility
2. Follow single responsibility principle
3. Consider module dependencies
4. Maintain high cohesion

**COMMON PATTERNS:**
- Database tasks → database/models module
- User-related tasks → auth/users module
- API endpoints → api/controllers module
- Business logic → services/core module
- Cross-cutting concerns → utils/middleware

**OUTPUT:**
Return ONLY the module name (no explanation, no quotes).