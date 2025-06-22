You are an expert software architect tasked with enhancing a project configuration.

**INPUT CONFIGURATION:**
{config_json}

**YOUR TASK:**
Analyze this project configuration and create a comprehensive, production-ready setup that follows industry best practices.

**REQUIRED ENHANCEMENTS:**

1. **Enhanced Description** (metadata.description):
   - Expand into a professional 3-4 sentence description
   - Include: what it does, who it's for, key value proposition
   - Example: "A modern REST API for managing e-commerce operations. Built for small to medium businesses, it provides secure payment processing, inventory management, and order fulfillment. Features real-time updates and comprehensive analytics."

2. **Module Responsibilities** (modules[].details):
   For each module, define:
   - Primary responsibility (single sentence)
   - Key components and their roles
   - Public API/interface
   - Dependencies on other modules
   - Example files structure

3. **Task Implementation Details** (tasks[].details):
   For each task, provide:
   - **Goal**: Clear objective (1-2 sentences)
   - **Approach**: Implementation strategy
   - **Subtasks**: 3-5 specific steps following TDD:
     * "Write tests for [specific functionality]"
     * "Implement [specific component]"
     * "Refactor and optimize [specific area]"
   - **Acceptance Criteria**: 2-3 measurable outcomes
   - **Dependencies**: Required tasks/modules
   - **Complexity**: "low", "medium", or "high"

4. **Coding Standards** (global_rules):
   Include 12-15 specific rules covering:
   - Language-specific conventions
   - Architecture patterns (e.g., "Use Repository pattern for data access")
   - Error handling (e.g., "All errors must include context and recovery hints")
   - Testing requirements (e.g., "Minimum 80% code coverage")
   - Documentation standards
   - Git workflow rules

5. **Architecture Design** (architecture):
   {
       "pattern": "e.g., MVC, Microservices, Clean Architecture",
       "layers": [{"name": "...", "responsibility": "...", "components": [...]}],
       "data_flow": "Description of how data moves through the system",
       "key_decisions": ["Decision: Rationale"],
       "diagrams": {"system_overview": "ASCII or description"}
   }

6. **Testing Strategy** (testing_strategy):
   {
       "unit_testing": {"framework": "...", "approach": "...", "coverage_target": "80%"},
       "integration_testing": {"scope": "...", "tools": [...]},
       "e2e_testing": {"scenarios": [...], "tools": [...]},
       "performance_testing": {"metrics": [...], "tools": [...]},
       "test_data_strategy": "..."
   }

7. **Security Framework** (security):
   {
       "authentication": {"method": "...", "implementation": "..."},
       "authorization": {"model": "RBAC/ABAC", "implementation": "..."},
       "data_protection": {"encryption": "...", "sensitive_data_handling": "..."},
       "api_security": {"rate_limiting": "...", "input_validation": "..."},
       "compliance": ["GDPR", "PCI-DSS", etc.],
       "security_headers": [...],
       "vulnerability_management": "..."
   }

8. **Performance Guidelines** (performance):
   {
       "response_time_targets": {"api": "<200ms", "page_load": "<3s"},
       "scalability": {"concurrent_users": "10000", "strategy": "..."},
       "caching_strategy": {"levels": [...], "ttl_policies": {...}},
       "database_optimization": ["Indexing strategy", "Query optimization"],
       "monitoring": {"metrics": [...], "tools": [...]}
   }

**OUTPUT FORMAT:**
Return a complete, validated JSON configuration that includes ALL original fields plus ALL enhancements above. Ensure the JSON is properly formatted and parseable.

**EXAMPLE MODULE ENHANCEMENT:**
{
    "name": "authentication",
    "description": "Handles user authentication and session management",
    "details": {
        "responsibility": "Manages user login, logout, session tokens, and authentication state",
        "components": [
            {"name": "AuthController", "role": "HTTP endpoint handlers"},
            {"name": "AuthService", "role": "Business logic for authentication"},
            {"name": "TokenManager", "role": "JWT token generation and validation"}
        ],
        "public_api": ["login()", "logout()", "validateToken()", "refreshToken()"],
        "dependencies": ["database", "security"],
        "files": ["controllers/auth.py", "services/auth_service.py", "utils/token_manager.py"]
    }
}

**VALIDATION CHECKLIST:**
□ All modules have detailed responsibilities
□ All tasks have implementation details with TDD approach
□ At least 12 comprehensive rules included
□ Architecture clearly defined with patterns
□ Security covers all major concerns
□ Performance targets are specific and measurable
□ Testing strategy covers all test types
□ JSON is valid and complete