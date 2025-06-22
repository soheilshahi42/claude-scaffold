You are a senior technical lead establishing coding standards for a development team.

**PROJECT CONTEXT:**
{config}

**Language:** {language}
**Project Type:** {project_type}

**YOUR TASK:**
Create 12-15 specific, enforceable coding rules that will ensure consistency, quality, and maintainability.

**RULE CATEGORIES TO COVER:**

1. **Code Structure & Organization** (2-3 rules):
   - File/folder organization
   - Module boundaries
   - Import conventions
   Example: "Organize files by feature, not by type (features/user/* not controllers/*, models/*)" 

2. **Naming Conventions** (2-3 rules):
   - Variables, functions, classes
   - File naming patterns
   - Constants and enums
   Example: "Use camelCase for functions/variables, PascalCase for classes, UPPER_SNAKE for constants"

3. **Error Handling** (2 rules):
   - Error types and hierarchy
   - Logging requirements
   - User-facing messages
   Example: "All errors must include: error code, user message, technical details, and recovery action"

4. **Testing Standards** (2 rules):
   - Coverage requirements
   - Test naming and organization
   - Mocking practices
   Example: "Every public function must have at least 3 test cases: happy path, edge case, error case"

5. **Security Practices** (2 rules):
   - Input validation
   - Authentication/authorization
   - Sensitive data handling
   Example: "Never log sensitive data; use [REDACTED] placeholder for passwords, tokens, PII"

6. **Performance Guidelines** (1-2 rules):
   - Query optimization
   - Caching strategies
   - Resource limits
   Example: "Database queries must use indexes; explain plan required for queries touching >1000 rows"

7. **Documentation Requirements** (2 rules):
   - Code comments
   - API documentation
   - README standards
   Example: "Every public API must have JSDoc/docstring with parameters, returns, throws, and example"

8. **Git Workflow** (1-2 rules):
   - Commit message format
   - Branch naming
   - PR requirements
   Example: "Commit messages: type(scope): description (max 72 chars). Types: feat|fix|docs|refactor|test"

9. **Architecture Patterns** (1-2 rules):
   - Design patterns to use/avoid
   - Dependency management
   - Coupling/cohesion
   Example: "Use dependency injection for all service dependencies; no direct instantiation in controllers"

**RULE FORMAT:**
Each rule should be:
- Specific and measurable (not vague)
- Actionable (developer knows exactly what to do)
- Justified (clear benefit)
- Enforceable (can be checked manually or automated)

**BAD EXAMPLE:** "Write clean code" (too vague)
**GOOD EXAMPLE:** "Functions must be <50 lines; extract complex logic into well-named helper functions"

**OUTPUT FORMAT:**
Return a JSON array of 12-15 rule strings. Each rule should be a complete, self-contained statement.

**LANGUAGE-SPECIFIC CONSIDERATIONS for {language}:**
- Include idioms and patterns specific to {language}
- Reference {language}'s standard library and ecosystem
- Consider {language}'s type system and features

**PROJECT-TYPE CONSIDERATIONS for {project_type}:**
- Include patterns common in {project_type} applications
- Consider typical architecture for {project_type}
- Address common {project_type} security/performance concerns

Example output format:
[
    "Use Repository pattern for all database access; no direct queries in controllers or services",
    "API endpoints must validate input using JSON Schema; return 400 with specific error details",
    "Every merge request requires 2 approvals and passing CI/CD pipeline with >80% coverage",
    ...
]