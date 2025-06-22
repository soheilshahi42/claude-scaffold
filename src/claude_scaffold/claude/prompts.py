"""
Prompts for Claude API interactions.

This module contains all prompts used for interacting with Claude API,
organized by their purpose and functionality. Each prompt is designed
to generate specific, actionable, and high-quality responses.

Prompt Design Principles:
- Clear context and purpose
- Specific output format requirements
- Examples where helpful
- Structured response format
- Explicit constraints and edge cases
"""

# Project Setup and Configuration Prompts

PROJECT_SETUP_ENHANCEMENT_PROMPT = """You are an expert software architect tasked with enhancing a project configuration.

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
   {{
       "pattern": "e.g., MVC, Microservices, Clean Architecture",
       "layers": [{{"name": "...", "responsibility": "...", "components": [...]}}],
       "data_flow": "Description of how data moves through the system",
       "key_decisions": ["Decision: Rationale"],
       "diagrams": {{"system_overview": "ASCII or description"}}
   }}

6. **Testing Strategy** (testing_strategy):
   {{
       "unit_testing": {{"framework": "...", "approach": "...", "coverage_target": "80%"}},
       "integration_testing": {{"scope": "...", "tools": [...]}},
       "e2e_testing": {{"scenarios": [...], "tools": [...]}},
       "performance_testing": {{"metrics": [...], "tools": [...]}},
       "test_data_strategy": "..."
   }}

7. **Security Framework** (security):
   {{
       "authentication": {{"method": "...", "implementation": "..."}},
       "authorization": {{"model": "RBAC/ABAC", "implementation": "..."}},
       "data_protection": {{"encryption": "...", "sensitive_data_handling": "..."}},
       "api_security": {{"rate_limiting": "...", "input_validation": "..."}},
       "compliance": ["GDPR", "PCI-DSS", etc.],
       "security_headers": [...],
       "vulnerability_management": "..."
   }}

8. **Performance Guidelines** (performance):
   {{
       "response_time_targets": {{"api": "<200ms", "page_load": "<3s"}},
       "scalability": {{"concurrent_users": "10000", "strategy": "..."}},
       "caching_strategy": {{"levels": [...], "ttl_policies": {{...}}}},
       "database_optimization": ["Indexing strategy", "Query optimization"],
       "monitoring": {{"metrics": [...], "tools": [...]}}
   }}

**OUTPUT FORMAT:**
Return a complete, validated JSON configuration that includes ALL original fields plus ALL enhancements above. Ensure the JSON is properly formatted and parseable.

**EXAMPLE MODULE ENHANCEMENT:**
{{
    "name": "authentication",
    "description": "Handles user authentication and session management",
    "details": {{
        "responsibility": "Manages user login, logout, session tokens, and authentication state",
        "components": [
            {{"name": "AuthController", "role": "HTTP endpoint handlers"}},
            {{"name": "AuthService", "role": "Business logic for authentication"}},
            {{"name": "TokenManager", "role": "JWT token generation and validation"}}
        ],
        "public_api": ["login()", "logout()", "validateToken()", "refreshToken()"],
        "dependencies": ["database", "security"],
        "files": ["controllers/auth.py", "services/auth_service.py", "utils/token_manager.py"]
    }}
}}

**VALIDATION CHECKLIST:**
□ All modules have detailed responsibilities
□ All tasks have implementation details with TDD approach
□ At least 12 comprehensive rules included
□ Architecture clearly defined with patterns
□ Security covers all major concerns
□ Performance targets are specific and measurable
□ Testing strategy covers all test types
□ JSON is valid and complete"""

TASK_DETAILS_GENERATION_PROMPT = """You are a senior software engineer creating a detailed implementation plan.

**TASK CONTEXT:**
- Task Name: {task_name}
- Module: {module_name}
- Project Type: {project_type}
- Programming Language: {language}

**YOUR MISSION:**
Create a comprehensive, actionable implementation plan that a developer can follow step-by-step.

**REQUIRED SECTIONS:**

1. **Goal Statement** (goal):
   - Clear, specific objective (1-2 sentences)
   - What success looks like
   - Example: "Implement secure JWT-based authentication that allows users to login with email/password and maintains sessions for 24 hours."

2. **Implementation Approach** (approach):
   - High-level strategy (2-3 sentences)
   - Key design decisions
   - Patterns or libraries to use

3. **Detailed Subtasks** (subtasks) - Follow TDD methodology:
   a. **Test Phase** (minimum 2 test tasks):
      - "Write unit tests for [specific functionality]"
      - "Create integration tests for [specific flow]"
   b. **Implementation Phase** (3-5 tasks):
      - "Create [specific component/class]"
      - "Implement [specific feature]"
      - "Integrate with [specific module]"
   c. **Refinement Phase** (1-2 tasks):
      - "Refactor for [specific improvement]"
      - "Add error handling for [edge cases]"

4. **Dependencies** (dependencies):
   - **Modules**: List of required modules
   - **Tasks**: List of tasks that must be completed first
   - **External**: Libraries, APIs, or services needed
   - **Knowledge**: Concepts that need to be understood

5. **Acceptance Criteria** (acceptance_criteria) - Minimum 3:
   - Specific, measurable outcomes
   - User-facing functionality
   - Technical requirements
   - Example: "Users can login with valid credentials and receive a JWT token"

6. **Technical Challenges** (challenges):
   - **Challenge**: Description
   - **Solution**: Proposed approach
   - **Fallback**: Alternative if primary solution fails

7. **Code Quality Checklist** (quality_checklist):
   - ☐ "All functions have comprehensive docstrings"
   - ☐ "Error handling covers all edge cases"
   - ☐ "Code follows project style guide"
   - ☐ "Performance optimized for expected load"
   - ☐ "Security best practices implemented"

8. **Research Topics** (research_needed):
   - Concepts to study before implementation
   - Documentation to review
   - Similar implementations to reference

9. **Estimated Complexity** (complexity):
   - Rating: "low" | "medium" | "high"
   - Reasoning: Why this complexity rating
   - Time estimate: Rough hours/days needed

**OUTPUT FORMAT:**
{{
    "goal": "Clear objective statement",
    "approach": "Implementation strategy",
    "subtasks": [
        "Test: Write unit tests for user validation",
        "Test: Create integration tests for login flow",
        "Implement: Create User model with validation",
        "Implement: Build authentication service",
        "Implement: Create login/logout endpoints",
        "Refactor: Optimize token generation",
        "Document: Add API documentation"
    ],
    "dependencies": {{
        "modules": ["database", "security"],
        "tasks": ["Setup database schema"],
        "external": ["bcrypt", "jsonwebtoken"],
        "knowledge": ["JWT best practices", "Password hashing"]
    }},
    "acceptance_criteria": [
        "Users can register with email and password",
        "Users can login and receive a valid JWT token",
        "Tokens expire after 24 hours",
        "Invalid credentials return appropriate error messages",
        "All passwords are hashed using bcrypt"
    ],
    "challenges": [
        {{
            "challenge": "Secure token storage",
            "solution": "Use httpOnly cookies with secure flag",
            "fallback": "Store in localStorage with XSS protection"
        }}
    ],
    "quality_checklist": [
        "All authentication functions have unit tests",
        "Password hashing uses salt rounds >= 10",
        "SQL injection prevention implemented",
        "Rate limiting on login endpoint"
    ],
    "research_needed": [
        "OWASP authentication best practices",
        "JWT vs session-based authentication trade-offs",
        "{language} specific security libraries"
    ],
    "complexity": {{
        "rating": "medium",
        "reasoning": "Involves security considerations and multiple components",
        "time_estimate": "2-3 days for full implementation"
    }}
}}

**IMPORTANT:**
- Be specific to {language} and {project_type}
- Include concrete examples, not generic statements
- Ensure all subtasks are actionable and testable
- Consider security implications for all features"""

MODULE_DOCUMENTATION_ENHANCEMENT_PROMPT = """You are a technical architect creating comprehensive module documentation.

**MODULE CONTEXT:**
- Module Name: {module_name}
- Current Description: {description}
- Project Type: {project_type}
- Language: {language}
- Related Modules: {other_modules}

**YOUR TASK:**
Create detailed, actionable documentation that serves as the definitive guide for this module.

**DOCUMENTATION STRUCTURE:**

1. **Overview** (overview):
   {{
       "purpose": "Clear statement of what this module does and why it exists",
       "scope": "What is included and explicitly excluded",
       "key_features": ["Feature 1", "Feature 2", ...]
   }}

2. **Architecture** (architecture):
   {{
       "design_pattern": "e.g., Repository, Service Layer, MVC",
       "components": [
           {{
               "name": "ComponentName",
               "type": "class|interface|service|utility",
               "responsibility": "What it does",
               "location": "path/to/component.{ext}"
           }}
       ],
       "data_flow": "How data moves through the module",
       "state_management": "How state is handled (if applicable)"
   }}

3. **Public API** (public_api):
   {{
       "endpoints": [
           {{
               "name": "functionName",
               "description": "What it does",
               "parameters": [{{"name": "param", "type": "string", "required": true, "description": "..."}}],
               "returns": {{"type": "Object", "description": "..."}},
               "throws": [{{"type": "ErrorType", "condition": "When..."}}],
               "example": "Code example"
           }}
       ],
       "events": [{{"name": "eventName", "payload": {{...}}, "when": "..."}}],
       "constants": [{{"name": "CONSTANT_NAME", "value": "...", "description": "..."}}]
   }}

4. **Dependencies** (dependencies):
   {{
       "internal_modules": [
           {{"module": "module_name", "purpose": "Why we depend on it", "interfaces_used": [...]}}
       ],
       "external_packages": [
           {{"package": "package_name", "version": "^1.0.0", "purpose": "...", "alternatives": [...]}}
       ],
       "system_requirements": ["Requirement 1", ...]
   }}

5. **Configuration** (configuration):
   {{
       "environment_variables": [
           {{"name": "VAR_NAME", "type": "string", "default": "...", "description": "..."}}
       ],
       "config_files": [{{"path": "config/module.json", "format": "JSON", "schema": {{...}}}}],
       "feature_flags": [{{"name": "FEATURE_NAME", "default": false, "description": "..."}}]
   }}

6. **Error Handling** (error_handling):
   {{
       "error_types": [
           {{
               "name": "ValidationError",
               "when": "Input validation fails",
               "recovery": "How to handle",
               "user_message": "What users see"
           }}
       ],
       "error_codes": [{{"code": "MOD_001", "meaning": "...", "action": "..."}}],
       "logging_strategy": "What gets logged and at what level"
   }}

7. **Performance** (performance):
   {{
       "optimization_strategies": ["Caching approach", "Query optimization", ...],
       "benchmarks": {{"operation": "Expected time/throughput"}},
       "resource_limits": {{"memory": "Max MB", "cpu": "Max %", "connections": "Max concurrent"}},
       "monitoring_points": ["What to monitor", ...]
   }}

8. **Security** (security):
   {{
       "authentication": "How authentication is handled",
       "authorization": "Permission model used",
       "data_validation": "Input sanitization approach",
       "sensitive_data": ["What data is sensitive and how it's protected"],
       "security_headers": ["Headers added by this module"],
       "rate_limiting": "If and how rate limiting is applied"
   }}

9. **Testing** (testing):
   {{
       "test_strategy": "Overall approach to testing this module",
       "test_categories": [
           {{"type": "unit", "location": "tests/unit/module_name", "coverage_target": "90%"}},
           {{"type": "integration", "location": "tests/integration/module_name", "key_scenarios": [...]}}
       ],
       "test_data": "How test data is managed",
       "mocking_strategy": "What gets mocked and how"
   }}

10. **Usage Examples** (examples):
    [
        {{
            "scenario": "Basic usage",
            "description": "How to perform common operation",
            "code": "// Complete code example\n// with proper error handling",
            "output": "Expected result"
        }}
    ]

11. **Extension Guide** (extension_guide):
    {{
        "extension_points": [
            {{"name": "Custom validator", "interface": "IValidator", "how_to": "..."}
        ],
        "plugin_system": "If applicable, how to create plugins",
        "event_hooks": [{{"event": "beforeSave", "purpose": "...", "example": "..."}}]
    }}

12. **Migration Guide** (migration):
    {{
        "from_version": "Previous version migration notes",
        "breaking_changes": ["List of breaking changes"],
        "deprecations": [{{"feature": "...", "replacement": "...", "removal_date": "..."}}]
    }}

**OUTPUT REQUIREMENTS:**
- Return complete JSON with ALL sections
- Use {language}-specific examples and patterns
- Include concrete, runnable code examples
- Reference actual file paths and component names
- Consider the module's role within {project_type} architecture
- Ensure consistency with other modules: {other_modules}

**QUALITY CHECKLIST:**
✓ All sections have detailed, specific content
✓ Code examples are complete and runnable
✓ Error scenarios are comprehensive
✓ Performance considerations are quantified
✓ Security measures are explicit
✓ Testing strategy is actionable"""

MODULE_DOCUMENTATION_REFINEMENT_PROMPT = """You are refining module documentation based on user feedback.

**CURRENT DOCUMENTATION:**
{current_doc}

**USER FEEDBACK:**
{feedback}

**REFINEMENT STRATEGY:**

1. **Analyze Feedback:**
   - What aspects need improvement?
   - What's working well (keep these)?
   - Are there missing sections?
   - Is something unclear or incorrect?

2. **Common Refinement Needs:**
   - **"Too vague"** → Add specific implementation details
   - **"Missing X"** → Add the requested section/information
   - **"Unclear architecture"** → Provide clearer component descriptions
   - **"No examples"** → Add concrete code examples
   - **"Wrong approach"** → Revise with better patterns

3. **Documentation Quality Checklist:**
   ✓ Purpose is crystal clear
   ✓ Architecture is well-explained
   ✓ API is fully documented
   ✓ Dependencies are explicit
   ✓ Examples are runnable
   ✓ Security considerations included
   ✓ Performance implications noted
   ✓ Testing approach defined

4. **Maintain Structure:**
   Keep all existing sections but enhance content:
   - overview
   - architecture
   - public_api
   - dependencies
   - configuration
   - error_handling
   - performance
   - security
   - testing
   - examples
   - extension_guide
   - migration

**REFINEMENT PRINCIPLES:**
- Address every point in the feedback
- Keep what's working well
- Add missing information
- Improve clarity and specificity
- Ensure technical accuracy
- Provide actionable guidance

**OUTPUT FORMAT:**
Return the complete module documentation JSON with all sections, incorporating the improvements requested in the feedback while maintaining the same structure.

**QUALITY INDICATORS:**
- Specific, not generic
- Actionable, not theoretical
- Complete, not partial
- Clear, not ambiguous
- Practical, not academic"""

GLOBAL_RULES_GENERATION_PROMPT = """You are a senior technical lead establishing coding standards for a development team.

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
]"""

PROJECT_CONFIGURATION_VALIDATION_PROMPT = """Review this project configuration for completeness and best practices:
{config_json}

Analyze the configuration and provide:
1. **Validation Results**: List any missing or incomplete sections
2. **Suggestions**: Specific improvements for each section
3. **Architecture Review**: Assessment of the proposed structure
4. **Risk Assessment**: Potential challenges or issues
5. **Enhanced Configuration**: Return the complete configuration with your improvements

Focus on:
- Completeness of module definitions
- Clarity of task descriptions
- Appropriateness of rules
- Architectural soundness
- Testing coverage
- Security considerations

Return a JSON object with your analysis and the enhanced configuration."""

# Batch Generation Prompts

MODULE_DESCRIPTION_BATCH_PROMPT = """You are creating concise, precise module descriptions for a development team.

**PROJECT CONTEXT:**
- Type: {project_type}
- Language: {language}
- Description: {project_description}

**MODULES TO DESCRIBE:**
{modules_list}

**DESCRIPTION REQUIREMENTS:**
1. Maximum 100 characters per description
2. Start with an action verb (Manages, Handles, Provides, Implements)
3. Specify WHAT it does, not HOW
4. Include the key domain concept
5. Be specific to {project_type} in {language}

**GOOD EXAMPLES:**
- "authentication": "Manages user login, JWT tokens, and session validation"
- "payment_processing": "Handles credit card transactions and payment webhooks"
- "data_pipeline": "Processes and transforms incoming data streams for analytics"

**BAD EXAMPLES:**
- "authentication": "Auth stuff" (too vague)
- "payment_processing": "Processes payments" (too generic)
- "data_pipeline": "Handles all the data pipeline functionality for the system" (too wordy)

**OUTPUT FORMAT:**
{{
    "module_name": "Clear, specific description under 100 chars",
    "module_name2": "Another description",
    ...
}}

**CONTEXT-SPECIFIC GUIDANCE:**
For {project_type} projects in {language}, consider:
- Common patterns and responsibilities in {project_type} architecture
- {language}-specific conventions and frameworks
- How these modules typically interact in {project_type} systems"""

TASK_DETAILS_BATCH_PROMPT = """You are a technical lead creating implementation plans for multiple development tasks.

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
{{
    "task_name": {{
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
    }},
    "next_task": {{ ... }}
}}

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
- Consider {project_type} security/performance requirements"""

# Q&A and Discovery Prompts

PROJECT_QUESTIONS_INITIAL_PROMPT = """You are an expert software architect conducting a discovery session. Your role is to ask insightful questions that uncover critical project requirements.

**PROJECT BRIEF:**
"{project_description}"

**YOUR TASK:**
Generate ONE highly strategic question that will reveal essential information for building this project successfully.

**QUESTION CRITERIA:**
1. **Specific**: Target a particular aspect, not general information
2. **Revealing**: The answer should significantly impact architecture or implementation
3. **Contextual**: Build on what's implied but not stated in the description
4. **Actionable**: The answer should directly inform development decisions

**CATEGORIES TO EXPLORE:** {categories}

**QUESTION PATTERNS BY CATEGORY:**

- **Technical Stack**: "What specific performance requirements (requests/sec, data volume, concurrent users) will drive our technology choices?"
- **Architecture**: "Should this system be designed for multi-tenancy, and if so, what level of data isolation is required?"
- **Features**: "Among the mentioned features, which 2-3 are absolutely critical for launch vs. nice-to-have for later phases?"
- **Integrations**: "What existing systems or APIs must this integrate with, and what are their constraints?"
- **Security**: "What compliance requirements (GDPR, HIPAA, PCI) or security standards must we meet?"
- **Users**: "Who are the primary vs. secondary user personas, and what are their technical proficiency levels?"
- **Constraints**: "What are the hard limits on budget, timeline, or team size that will affect our approach?"

**OUTPUT FORMAT:**
{{
    "question": "Your specific, revealing question here",
    "category": "{categories}",
    "importance": "high|medium|low",
    "reason": "How the answer will impact development decisions",
    "follow_ups": ["Potential follow-up question 1", "Potential follow-up question 2"]
}}

**EXAMPLE OUTPUT:**
{{
    "question": "Will this e-commerce platform need to handle digital products, physical inventory, or both, and what are the expected transaction volumes per day?",
    "category": "Architecture",
    "importance": "high",
    "reason": "Determines whether we need inventory management, fulfillment integration, and the database architecture for handling different product types and scale",
    "follow_ups": ["What payment providers need to be integrated?", "Are there specific shipping/fulfillment partners?"]
}}

**AVOID:**
- Yes/no questions
- Questions already answered in the description
- Generic questions that apply to any project
- Multiple questions disguised as one"""

PROJECT_QUESTIONS_CONTEXTUAL_PROMPT = """You are a senior architect conducting an in-depth discovery session. Your goal is to systematically uncover all critical information needed for successful project delivery.

**PROJECT CONTEXT:**
Description: "{project_description}"

**CONVERSATION HISTORY:**
{qa_context}

**YOUR MISSION:**
Analyze what has been discussed and identify the MOST CRITICAL gap in our understanding. Generate ONE strategic question that fills this gap.

**DISCOVERY CATEGORIES WITH STRATEGIC QUESTIONS:**

1. **Technical Stack** ✓ Priority: HIGH
   - "What are the specific version requirements for frameworks/languages?"
   - "Are there legacy systems we must maintain compatibility with?"
   - "What are the non-negotiable technology constraints?"

2. **Architecture** ✓ Priority: HIGH
   - "What's the expected system load (users, requests/sec, data volume)?"
   - "Do we need real-time features, and if so, for which components?"
   - "How should the system handle failure scenarios and data consistency?"

3. **Features** ✓ Priority: HIGH
   - "What's the MVP feature set vs. the complete vision?"
   - "Which features have complex business logic that needs clarification?"
   - "What are the deal-breaker features for launch?"

4. **UI/UX** ≡ Priority: MEDIUM
   - "Do you have existing design systems or brand guidelines to follow?"
   - "What devices/browsers must be supported with what level of experience?"
   - "Are there specific accessibility requirements (WCAG level)?"

5. **Authentication** ✓ Priority: HIGH
   - "What authentication methods are required (SSO, 2FA, social login)?"
   - "How complex is the authorization model (roles, permissions, teams)?"
   - "Are there specific session management requirements?"

6. **Data Model** ✓ Priority: HIGH
   - "What's the expected data volume and growth rate?"
   - "Are there complex relationships or reporting requirements?"
   - "What are the data retention and archival policies?"

7. **API Design** ≡ Priority: MEDIUM
   - "Will this API be public-facing or internal only?"
   - "What are the rate limiting and quota requirements?"
   - "Do we need versioning strategy for backward compatibility?"

8. **Integrations** ✓ Priority: HIGH
   - "What third-party services are mandatory vs. optional?"
   - "What are the data synchronization requirements?"
   - "Are there specific API limitations we should know about?"

9. **Performance** ≡ Priority: MEDIUM
   - "What are the specific SLA requirements (uptime, response time)?"
   - "What's the expected geographic distribution of users?"
   - "Are there specific bottlenecks from past experiences?"

10. **Security** ✓ Priority: HIGH
    - "What compliance standards must we meet (SOC2, HIPAA, PCI)?"
    - "What's the data classification and encryption requirements?"
    - "Have you had security audits that revealed specific concerns?"

11. **Deployment** ≡ Priority: MEDIUM
    - "What's your preferred cloud provider and region constraints?"
    - "Do you need multi-region deployment or disaster recovery?"
    - "What are the DevOps practices currently in place?"

12. **Timeline** ✓ Priority: HIGH
    - "What's driving the timeline - market opportunity, compliance, competition?"
    - "Are there hard deadlines vs. soft targets?"
    - "What's the budget range and team size constraints?"

13. **Testing** ≡ Priority: MEDIUM
    - "What's the current QA process and tools?"
    - "Are there specific compliance testing requirements?"
    - "What's the acceptable defect tolerance for launch?"

14. **Error Handling** ≡ Priority: LOW
    - "What monitoring and alerting systems are in place?"
    - "What's the incident response process?"
    - "Are there specific uptime or recovery requirements?"

15. **Documentation** ≡ Priority: LOW
    - "Who are the documentation audiences (developers, users, admins)?"
    - "Are there regulatory documentation requirements?"
    - "What's the preferred documentation platform?"

16. **Future Extensibility** ≡ Priority: MEDIUM
    - "What's the 2-year vision for this product?"
    - "Are there known future integrations or markets?"
    - "What technical debt is acceptable for initial launch?"

**INTELLIGENT QUESTION SELECTION RULES:**

1. **Coverage Analysis**: Check which categories have NO questions asked yet
2. **Dependency Chain**: Ask about prerequisites before dependent features
3. **Risk Priority**: Focus on high-impact unknowns that could derail the project
4. **Depth vs. Breadth**: If major areas are covered, go deeper into critical ones
5. **Context Building**: Each question should build on previous answers

**QUESTION QUALITY CHECKLIST:**
☐ Not already answered in previous Q&A
☐ Reveals information that affects multiple development decisions
☐ Specific enough to get actionable details
☐ Cannot be answered with yes/no
☐ Addresses current highest-priority unknown

**OUTPUT FORMAT:**
{{
    "question": "Your strategic question that addresses the most critical current gap",
    "category": "Category from list above",
    "importance": "high|medium|low",
    "reason": "Specific development decisions this will inform",
    "depends_on": ["Categories that should be clear before asking this"],
    "unlocks": ["What categories/decisions this answer will enable"]
}}

**EXAMPLE:**
{{
    "question": "For user authentication, do you need single sign-on (SSO) integration with specific providers like Okta or Auth0, and will you need to support multiple tenants with isolated data?",
    "category": "Authentication",
    "importance": "high",
    "reason": "Determines whether we need SAML/OAuth implementation, affects database architecture for multi-tenancy, and impacts our choice of authentication libraries",
    "depends_on": ["Architecture", "Technical Stack"],
    "unlocks": ["Data Model", "Security", "API Design"]
}}"""

QA_COMPILATION_TO_SPEC_PROMPT = """
You are a senior technical architect creating a comprehensive technical specification from a discovery session.

**ORIGINAL PROJECT BRIEF:**
"{project_description}"

**DISCOVERY SESSION TRANSCRIPT:**
{qa_text}

**YOUR TASK:**
Synthesize all gathered information into a professional technical specification that serves as the definitive guide for the development team.

**TECHNICAL SPECIFICATION STRUCTURE:**

# PROJECT: [Extracted Project Name]

## 1. EXECUTIVE SUMMARY
- **Vision**: Enhanced 2-3 sentence description incorporating all insights
- **Primary Goal**: The main problem this solves
- **Target Users**: Specific user segments identified
- **Success Metrics**: How we'll measure success
- **Key Differentiators**: What makes this unique

## 2. TECHNICAL ARCHITECTURE

### 2.1 System Architecture
- **Pattern**: (e.g., Microservices, Monolithic, Serverless)
- **Key Components**: List with responsibilities
- **Data Flow**: How information moves through the system
- **Scalability Strategy**: How system grows with load

### 2.2 Technology Stack
```
Frontend:
  - Framework: [Name + Version]
  - State Management: [Tool]
  - UI Library: [Name]
  - Build Tools: [List]

Backend:
  - Language: [Name + Version]
  - Framework: [Name]
  - Database: [Type + Specific DB]
  - Cache: [Redis/Memcached/etc]
  - Message Queue: [If applicable]

Infrastructure:
  - Cloud Provider: [AWS/GCP/Azure]
  - Container: [Docker/K8s]
  - CI/CD: [Tools]
  - Monitoring: [Tools]
```

### 2.3 Database Design
- **Type**: (Relational/NoSQL/Hybrid)
- **Key Entities**: [List with relationships]
- **Scaling Strategy**: (Sharding/Replication/etc)
- **Backup/Recovery**: Approach

## 3. FEATURE SPECIFICATIONS

### 3.1 Core Features (MVP)
1. **[Feature Name]**
   - Description: What it does
   - User Story: As a [user], I want to [action] so that [benefit]
   - Acceptance Criteria: Bullet list
   - Priority: P0 (Critical)

### 3.2 Phase 2 Features
[Similar structure for post-MVP features]

## 4. API DESIGN

### 4.1 API Architecture
- **Style**: REST/GraphQL/gRPC
- **Versioning**: Strategy
- **Authentication**: Method (JWT/OAuth/etc)
- **Rate Limiting**: Limits and strategy

### 4.2 Key Endpoints
```
[Method] /api/v1/[resource]
Description: What it does
Auth: Required/Optional
Request: { example }
Response: { example }
```

## 5. USER INTERFACE

### 5.1 Design Principles
- **Style**: (Material/Custom/etc)
- **Responsive**: Breakpoints and approach
- **Accessibility**: WCAG level and requirements
- **Browser Support**: Minimum versions

### 5.2 Key User Flows
1. **[Flow Name]**: Step-by-step description

## 6. SECURITY FRAMEWORK

### 6.1 Authentication & Authorization
- **Authentication**: Method and flow
- **Authorization**: Model (RBAC/ABAC)
- **Session Management**: Approach

### 6.2 Data Protection
- **Encryption**: At rest and in transit
- **PII Handling**: How sensitive data is managed
- **Compliance**: GDPR/HIPAA/PCI requirements

### 6.3 Security Measures
- Input validation
- SQL injection prevention
- XSS protection
- CSRF tokens
- Rate limiting

## 7. DEPLOYMENT & INFRASTRUCTURE

### 7.1 Environments
- **Development**: Setup and access
- **Staging**: Mirrors production
- **Production**: High-level architecture

### 7.2 CI/CD Pipeline
1. Code commit triggers build
2. Automated tests run
3. Security scanning
4. Deploy to staging
5. Manual approval
6. Production deployment

### 7.3 Monitoring & Logging
- **APM**: Tool and key metrics
- **Logging**: Centralized logging solution
- **Alerts**: Critical alerts defined

## 8. PERFORMANCE REQUIREMENTS

### 8.1 Performance Targets
- **Response Time**: <200ms for API calls
- **Throughput**: X requests/second
- **Concurrent Users**: Y users
- **Data Volume**: Z GB/day

### 8.2 Optimization Strategies
- Caching layers
- CDN usage
- Database indexing
- Code optimization areas

## 9. TESTING STRATEGY

### 9.1 Test Levels
- **Unit Tests**: >80% coverage
- **Integration Tests**: Key flows
- **E2E Tests**: Critical paths
- **Performance Tests**: Load scenarios

### 9.2 Test Automation
- Tools and frameworks
- Continuous testing in CI/CD
- Test data management

## 10. PROJECT CONSTRAINTS & TIMELINE

### 10.1 Constraints
- **Budget**: Range if mentioned
- **Team Size**: Available resources
- **Technical Debt**: Acceptable trade-offs
- **Legal/Compliance**: Requirements

### 10.2 Development Phases
1. **Phase 1 (MVP)**: [Duration] - [Key deliverables]
2. **Phase 2**: [Duration] - [Key deliverables]
3. **Phase 3**: [Duration] - [Key deliverables]

### 10.3 Risks & Mitigation
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk description] | High/Med/Low | High/Med/Low | [Strategy] |

## 11. THIRD-PARTY INTEGRATIONS

### 11.1 Required Integrations
- **[Service Name]**: Purpose and integration method
- **API Limits**: Rate limits and quotas
- **Fallback**: What happens if service fails

## 12. FUTURE ROADMAP

### 12.1 Planned Enhancements
- 6 months: [Features]
- 1 year: [Features]
- 2 years: [Vision]

### 12.2 Scalability Considerations
- Technical scaling points
- Business scaling considerations
- International expansion needs

## APPENDICES

### A. Glossary
Define project-specific terms

### B. References
Links to relevant documentation

### C. Decision Log
Key technical decisions made during discovery

---

**SPECIFICATION METADATA:**
- Version: 1.0
- Date: [Today]
- Status: Draft/Approved
- Next Review: [Date]

**COMPILATION RULES:**
1. Extract specific details from Q&A responses
2. Organize information logically, not chronologically
3. Resolve contradictions using most recent/detailed answers
4. Flag any critical unknowns as "TBD: [what's needed]"
5. Include reasonable defaults for unmentioned standard practices
6. Ensure technical consistency throughout
7. Make it actionable - developers should know exactly what to build

**QUALITY CHECKLIST:**
✓ All Q&A insights incorporated
✓ No contradictions or ambiguities
✓ Technical choices justified
✓ Estimates are realistic
✓ Risks are identified
✓ Success criteria are measurable
"""

# Interactive Enhancement Prompts

DESCRIPTION_ENHANCEMENT_PROMPT = """You are enhancing a project description to be more professional and comprehensive.

**CURRENT DESCRIPTION:**
{description}

**YOUR TASK:**
Transform this into a compelling, professional project description that clearly communicates value and scope.

**DESCRIPTION FRAMEWORK:**

1. **What** - Core functionality in specific terms
2. **Who** - Target audience with clear personas
3. **Why** - The problem it solves or value it provides
4. **How** - Key technical approach or differentiator
5. **Result** - The outcome or benefit for users

**FORMULA:**
"[Product] is a [type] that [core function] for [target audience]. It [key feature/approach] to [solve problem/provide value], enabling [key benefit/outcome]. Built with [notable tech], it [unique differentiator]."

**GOOD EXAMPLES:**

✓ "TaskFlow is a project management platform that streamlines agile workflows for distributed software teams. It uses AI-powered sprint planning to reduce estimation errors by 40%, enabling teams to deliver more predictable results. Built with React and GraphQL, it integrates seamlessly with existing developer tools."

✓ "SecureVault is a password management system that provides enterprise-grade security for small businesses. It uses zero-knowledge encryption to protect sensitive credentials while maintaining ease of use, enabling teams to follow security best practices without friction. Built with Rust for maximum performance and security."

**BAD EXAMPLES:**

✗ "A project management tool" (too vague)
✗ "This is a system for managing projects with lots of features" (no specifics)
✗ "An app that helps teams work better" (no clear value prop)

**REQUIREMENTS:**
- Length: 2-4 sentences (60-120 words)
- Tone: Professional but approachable
- Include specific benefits or metrics if relevant
- Mention key technologies only if they add value
- Focus on outcomes, not just features

**OUTPUT:**
Return ONLY the enhanced description text, no additional commentary."""

MODULE_SUGGESTIONS_PROMPT = """You are a software architect designing the module structure for a new project using industry best practices from clean architecture, domain-driven design, and modern software engineering principles.

**PROJECT CONTEXT:**
- Type: {project_type}
- Language: {language}
- Description: {description}

**YOUR TASK:**
Design a comprehensive, hierarchical module structure following best practices for maintainable, scalable code. Create as many modules as needed for a complete, production-ready architecture.

**CORE ARCHITECTURAL PRINCIPLES:**

1. **Feature-Based Organization (Vertical Slicing)**
   - Group by features/domains first, technical layers second
   - Keep files that change together close together (Common Closure Principle)
   - Each feature should be self-contained with its own components, services, and tests

2. **Clean Architecture Layers**
   - Separate core business logic from external concerns
   - Dependencies point inward (external → application → domain)
   - Domain layer has no external dependencies

3. **Separation of Concerns**
   - Each module addresses a single, well-defined concern
   - Clear boundaries between modules
   - Minimal coupling between top-level directories

4. **Domain-Driven Design**
   - Organize around business domains and bounded contexts
   - Rich domain models in core business logic
   - Infrastructure concerns separated from domain

**RECOMMENDED STRUCTURE PATTERNS:**

**Full-Stack Application (Monorepo):**
```
src/
├── domain/                      # Core business logic (no external dependencies)
│   ├── user/
│   │   ├── entities/
│   │   ├── values/
│   │   └── services/
│   ├── product/
│   │   ├── entities/
│   │   ├── values/
│   │   └── rules/
│   └── shared/
│       ├── types/
│       └── exceptions/
├── application/                 # Use cases and application logic
│   ├── user/
│   │   ├── commands/           # State-changing operations
│   │   ├── queries/            # Data retrieval
│   │   └── handlers/
│   ├── product/
│   │   ├── commands/
│   │   ├── queries/
│   │   └── dto/
│   └── shared/
│       └── interfaces/
├── infrastructure/              # External concerns
│   ├── persistence/
│   │   ├── repositories/
│   │   ├── migrations/
│   │   └── models/
│   ├── messaging/
│   │   ├── publishers/
│   │   └── consumers/
│   ├── external/
│   │   ├── payment/
│   │   └── email/
│   └── web/
│       ├── api/
│       │   ├── rest/
│       │   └── graphql/
│       └── middleware/
├── presentation/                # UI Layer
│   ├── web/
│   │   ├── pages/
│   │   ├── features/
│   │   │   ├── user/
│   │   │   │   ├── components/
│   │   │   │   ├── hooks/
│   │   │   │   └── services/
│   │   │   └── product/
│   │   │       ├── components/
│   │   │       └── services/
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   ├── layouts/
│   │   │   └── utils/
│   │   └── assets/
│   └── mobile/
│       └── [similar structure]
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── tools/
    ├── scripts/
    └── config/
```

**Microservices Architecture:**
```
services/
├── user-service/
│   ├── src/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── api/
│   ├── tests/
│   └── docs/
├── product-service/
│   └── [similar structure]
├── order-service/
│   └── [similar structure]
├── notification-service/
│   └── [similar structure]
shared/
├── contracts/           # Shared API contracts
├── events/             # Event definitions
├── errors/             # Common error types
└── utils/              # Shared utilities
infrastructure/
├── api-gateway/
├── service-discovery/
├── monitoring/
└── deployment/
frontend/
├── web/
│   ├── features/
│   ├── shared/
│   └── core/
└── mobile/
    └── [similar structure]
```

**Enterprise/Clean Architecture:**
```
src/
├── core/                       # Business logic layer
│   ├── domain/
│   │   ├── aggregates/
│   │   ├── entities/
│   │   ├── values/
│   │   ├── events/
│   │   └── specifications/
│   ├── application/
│   │   ├── interfaces/
│   │   ├── use-cases/
│   │   └── services/
│   └── shared-kernel/
├── adapters/                   # Interface adapters
│   ├── primary/               # Driving adapters
│   │   ├── web-api/
│   │   ├── cli/
│   │   └── message-queue/
│   └── secondary/             # Driven adapters
│       ├── persistence/
│       ├── external-apis/
│       └── file-storage/
├── frameworks/                 # Frameworks & drivers
│   ├── web/
│   ├── database/
│   └── messaging/
└── cross-cutting/             # Cross-cutting concerns
    ├── logging/
    ├── security/
    ├── monitoring/
    └── caching/
```

**MODULE NAMING CONVENTIONS:**

1. **Path Format**: Use forward slashes (domain/user/entities)
2. **Naming Style**: 
   - {language} conventions (snake_case for Python, kebab-case for JS/TS)
   - Descriptive names indicating purpose
   - Avoid generic names (utils, helpers, common) without context

3. **Hierarchy Rules**:
   - Layer/Concern → Domain/Feature → Technical Aspect
   - Examples: 
     - domain/user/entities
     - application/auth/commands
     - infrastructure/persistence/repositories

**BEST PRACTICES TO FOLLOW:**

1. **Keep Structure Reasonably Flat**
   - Maximum 4-5 levels deep
   - Too much nesting impedes navigation

2. **Feature Cohesion**
   - All files for a feature live together
   - Includes components, services, tests, styles

3. **Shared Code Organization**
   - Truly shared code in dedicated shared/ directories
   - Avoid premature abstraction
   - Copy-paste is sometimes better than wrong abstraction

4. **Test Proximity**
   - Unit tests near the code they test
   - Integration/E2E tests in separate test directories

5. **Documentation**
   - Each major module should have its own docs/
   - API documentation near API definitions

**{project_type} SPECIFIC CONSIDERATIONS:**
- Apply patterns suitable for {project_type}
- Consider scale and complexity of {project_type}
- Include modules specific to {project_type} requirements

**{language} SPECIFIC PATTERNS:**
- Follow {language} community standards
- Use {language} appropriate module systems
- Consider {language} framework conventions

**OUTPUT FORMAT:**
Return a JSON array of ALL module paths needed for a complete system:

[
  "src/domain/user/entities",
  "src/domain/user/values",
  "src/domain/user/services",
  "src/application/user/commands",
  "src/application/user/queries",
  "src/infrastructure/persistence/repositories",
  ...
]

**IMPORTANT GUIDELINES:**
- Include ALL modules for production readiness (typically 30-80+ paths)
- Start with core domain modules, then application, then infrastructure
- Consider team boundaries and deployment units
- Include supporting modules: testing, documentation, deployment
- Think about both current needs and 6-month growth

**AVOID:**
- Over-engineering for simple CRUD apps
- Flat structure when hierarchy would clarify relationships  
- Deep nesting beyond 5 levels
- Mixing different architectural patterns inconsistently
- Technology-specific names in domain layer"""

MODULE_DESCRIPTION_PROMPT = """Generate a precise module description.

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
Return ONLY the description text (no quotes, no formatting)."""

TASK_SUGGESTIONS_PROMPT = """You are a technical project manager creating a comprehensive task list for a new project.

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
]"""

MODULE_ASSIGNMENT_PROMPT = """Determine the most appropriate module for a task.

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
Return ONLY the module name (no explanation, no quotes)."""

RULE_SUGGESTIONS_PROMPT = """You are establishing coding standards and best practices for a development team.

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
- Generic rules that apply to any project"""

TECHNICAL_CONSTRAINTS_PROMPT = """You are identifying technical constraints and requirements for a new project.

**PROJECT DETAILS:**
- Type: {project_type}
- Language: {language}
- Description: {description}

**YOUR TASK:**
Identify likely technical constraints, requirements, and considerations that will impact development.

**CONSTRAINT CATEGORIES TO ANALYZE:**

1. **Language & Runtime**
   - Minimum version requirements
   - Runtime environment needs
   - Language-specific limitations

2. **Dependencies & Libraries**
   - Critical third-party packages
   - Version compatibility requirements
   - License considerations

3. **Performance Requirements**
   - Response time expectations
   - Throughput needs
   - Resource limits (CPU, memory)
   - Scalability requirements

4. **Security Constraints**
   - Authentication requirements
   - Data encryption needs
   - Compliance standards
   - Security headers/policies

5. **Infrastructure & Deployment**
   - Hosting environment
   - Container requirements
   - Database choices
   - CDN/caching needs

6. **Integration Requirements**
   - Third-party APIs
   - Legacy system compatibility
   - Data format standards
   - Protocol requirements

7. **Development Constraints**
   - Team size/expertise
   - Timeline pressures
   - Budget limitations
   - Tooling requirements

8. **Operational Requirements**
   - Uptime SLA
   - Backup/recovery needs
   - Monitoring requirements
   - Support considerations

**OUTPUT FORMAT:**
{{
    "runtime": {{
        "language_version": "Minimum required version",
        "environment": "Required runtime environment",
        "platform": "OS/platform constraints"
    }},
    "dependencies": {{
        "core_libraries": ["lib:version", ...],
        "compatibility": "Version constraints",
        "licenses": "License requirements"
    }},
    "performance": {{
        "response_time": "Target latency",
        "concurrent_users": "Expected load",
        "data_volume": "Storage needs",
        "availability": "Uptime requirement"
    }},
    "security": {{
        "authentication": "Auth requirements",
        "encryption": "Data protection needs",
        "compliance": ["Standards to meet"],
        "vulnerabilities": "Security considerations"
    }},
    "infrastructure": {{
        "hosting": "Deployment platform",
        "database": "Data storage needs",
        "caching": "Performance optimization",
        "cdn": "Content delivery needs"
    }},
    "integrations": {{
        "external_apis": ["Required integrations"],
        "data_formats": ["Supported formats"],
        "protocols": ["Communication protocols"]
    }},
    "development": {{
        "team_size": "Resource constraints",
        "expertise_required": ["Skill requirements"],
        "tooling": ["Development tools"],
        "timeline": "Time constraints"
    }},
    "operations": {{
        "monitoring": "Observability needs",
        "backup": "Data protection strategy",
        "support": "Maintenance requirements",
        "documentation": "Documentation needs"
    }}
}}

**CONSIDER {project_type} SPECIFICS:**
- Common {project_type} requirements
- Typical {project_type} constraints
- {project_type} best practices

**CONSIDER {language} SPECIFICS:**
- {language} ecosystem constraints
- Common {language} deployment patterns
- {language} performance characteristics"""

BUILD_COMMANDS_PROMPT = """You are a DevOps engineer setting up standard build commands for a project.

**PROJECT DETAILS:**
- Type: {project_type}
- Language: {language}

**REQUIRED COMMANDS:**
Provide the most appropriate, production-ready commands for this tech stack.

**COMMAND CATEGORIES:**

1. **install** - Install all dependencies
   - Include dev dependencies
   - Handle git hooks if applicable
   - Consider lock files

2. **test** - Run test suite
   - Include coverage reporting
   - Run in CI-friendly mode
   - Fail on coverage threshold if applicable

3. **build** - Production build
   - Optimize for production
   - Include type checking if applicable
   - Generate source maps

4. **dev** - Development server
   - Hot reload enabled
   - Debug mode
   - Source maps

5. **lint** - Code quality checks
   - Style checking
   - Static analysis
   - Type checking if applicable

6. **format** - Auto-format code
   - Apply project style
   - Fix auto-fixable issues

7. **clean** - Clean build artifacts
   - Remove dist/build folders
   - Clear cache

8. **validate** - Pre-commit validation
   - Run lint + test
   - Type check
   - Build check

**LANGUAGE-SPECIFIC EXAMPLES:**

For Node.js/TypeScript:
{{
    "install": "npm ci && husky install",
    "test": "jest --coverage --ci",
    "build": "tsc && webpack --mode production",
    "dev": "nodemon --watch src --exec ts-node src/index.ts",
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --write \"src/**/*.{ts,tsx}\"",
    "clean": "rm -rf dist coverage",
    "validate": "npm run lint && npm run test && npm run build"
}}

For Python:
{{
    "install": "pip install -r requirements.txt -r requirements-dev.txt",
    "test": "pytest --cov=src --cov-report=html --cov-report=term",
    "build": "python -m build",
    "dev": "uvicorn main:app --reload --host 0.0.0.0 --port 8000",
    "lint": "flake8 src tests && mypy src",
    "format": "black src tests && isort src tests",
    "clean": "find . -type d -name __pycache__ -exec rm -rf {{}} + && rm -rf dist build *.egg-info",
    "validate": "make lint && make test"
}}

**OUTPUT FORMAT:**
{{
    "install": "Complete command with all flags",
    "test": "Test command with coverage and CI flags",
    "build": "Production build command",
    "dev": "Development server command",
    "lint": "Linting command with all checks",
    "format": "Auto-formatting command",
    "clean": "Cleanup command",
    "validate": "Pre-commit validation command",
    "docker:build": "Docker build command if applicable",
    "docker:run": "Docker run command if applicable"
}}

**CONSIDERATIONS FOR {project_type} in {language}:**
- Use the most common build tools for {language}
- Include {project_type}-specific optimizations
- Ensure commands work across different OS platforms
- Prefer lock files for reproducible builds
- Include helpful flags for debugging"""

# Configuration Enhancement Prompts

CONFIGURATION_REFINEMENT_PROMPT = """You are refining a project configuration based on user feedback.

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
{{
    "refinement_summary": "Brief description of changes made",
    "modules": {{
        "added": [{{"name": "...", "description": "...", "reason": "Why added"}}],
        "modified": [{{"name": "...", "changes": "What changed", "reason": "Why"}}],
        "removed": [{{"name": "...", "reason": "Why removed"}}]
    }},
    "tasks": {{
        "added": [{{"name": "...", "module": "...", "description": "..."}}],
        "modified": [{{"name": "...", "changes": "..."}}],
        "removed": [{{"name": "...", "reason": "..."}}]
    }},
    "rules": {{
        "added": ["New rule 1", "New rule 2"],
        "modified": [{{"old": "...", "new": "...", "reason": "..."}}],
        "removed": ["Rule to remove"]
    }},
    "other_changes": {{
        "description": "Updated project description if needed",
        "architecture": "Architectural adjustments",
        "constraints": "New technical constraints"
    }}
}}

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
- "Combine these" → Merge with clear new structure"""

# Refinement Prompts

TEXT_REFINEMENT_PROMPT = """You are refining text based on specific user feedback.

**CURRENT TEXT:**
{current_value}

**USER FEEDBACK:**
{feedback}

**REFINEMENT GUIDELINES:**

1. **Analyze Feedback Type:**
   - Clarity issue → Simplify and clarify
   - Too generic → Add specifics and examples
   - Too verbose → Condense while keeping key info
   - Wrong focus → Shift emphasis appropriately
   - Missing info → Add requested details

2. **Maintain:**
   - Original intent and purpose
   - Appropriate tone and style
   - Any constraints (length, format)

3. **Improve:**
   - Address the specific issue raised
   - Enhance overall quality
   - Fix any other obvious issues

**OUTPUT:**
Return ONLY the improved text (no explanation or commentary)."""

LIST_REFINEMENT_PROMPT = """You are refining a list based on user feedback.

**CURRENT LIST:**
{current_items}

**USER FEEDBACK:**
{feedback}

**REFINEMENT STRATEGIES:**

1. **Common Feedback Patterns:**
   - "Too few" → Add more relevant items
   - "Too many" → Remove less important ones
   - "Wrong focus" → Replace with better alternatives
   - "Too generic" → Make items more specific
   - "Missing X" → Add the specific requested items

2. **List Quality Principles:**
   - Each item should be distinct and valuable
   - Order by importance or logical sequence
   - Consistent level of detail
   - No redundancy or overlap

3. **Improvement Process:**
   - Keep good items from original
   - Address specific feedback
   - Enhance overall quality
   - Maintain appropriate length

**OUTPUT FORMAT:**
Return a JSON array with improved items:
["item1", "item2", ...]

**ENSURE:**
- Valid JSON format
- Appropriate number of items
- Directly addresses feedback
- Maintains or improves quality"""

DICT_REFINEMENT_PROMPT = """You are refining structured data based on user feedback.

**CURRENT DATA:**
{current_data}

**USER FEEDBACK:**
{feedback}

**REFINEMENT APPROACH:**

1. **Understand the Feedback:**
   - Which fields need modification?
   - What improvements are requested?
   - Are there missing keys or values?

2. **Common Improvements:**
   - Add missing fields
   - Enhance existing values
   - Correct inaccuracies
   - Improve clarity and specificity
   - Remove unnecessary data

3. **Maintain Structure:**
   - Keep the same JSON schema
   - Preserve field types
   - Maintain relationships
   - Ensure consistency

**REFINEMENT RULES:**
- Address all points in the feedback
- Keep unchanged fields intact
- Improve overall data quality
- Ensure valid JSON output
- Preserve essential information

**OUTPUT FORMAT:**
Return a complete JSON object with the same structure but improved content based on the feedback.

**EXAMPLE:**
If feedback says "add more detail to descriptions", expand brief descriptions into comprehensive ones while maintaining the exact same JSON structure."""