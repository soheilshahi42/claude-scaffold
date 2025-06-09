"""
Prompts for Claude API interactions.

This module contains all prompts used for interacting with Claude API,
organized by their purpose and functionality.
"""

# Project Setup and Configuration Prompts

PROJECT_SETUP_ENHANCEMENT_PROMPT = """Based on this project configuration:
{config_json}

Analyze the project requirements and provide a comprehensive configuration that includes:

1. **Enhanced Description**: A more detailed and professional project description
2. **Module Responsibilities**: Clear definition of what each module should handle
3. **Task Details**: Specific implementation details for each task, including:
   - Clear goals and requirements
   - Implementation approach
   - Subtasks (following TDD: test first, then implementation)
   - Acceptance criteria
4. **Rules**: Project-specific coding standards and best practices
5. **Architecture**: Recommended architecture patterns and structure
6. **Testing Strategy**: Approach to testing (unit, integration, e2e)
7. **Security Considerations**: Security best practices for this type of project
8. **Performance Guidelines**: Performance optimization strategies

Return a complete project configuration JSON that includes all the original fields plus your enhancements.
The JSON should follow this structure:
{{
    "project_name": "...",
    "metadata": {{...enhanced...}},
    "structure": {{...enhanced with your recommendations...}},
    "modules": [...enhanced with detailed descriptions...],
    "tasks": [...enhanced with implementation details...],
    "global_rules": [...comprehensive list...],
    "architecture": {{...your recommendations...}},
    "testing_strategy": {{...}},
    "security": {{...}},
    "performance": {{...}}
}}

Make sure each module has:
- Clear responsibility boundaries
- Detailed description
- Key files and their purposes
- Dependencies on other modules

Make sure each task has:
- Implementation approach
- Subtasks with test-first approach
- Acceptance criteria
- Estimated complexity"""

TASK_DETAILS_GENERATION_PROMPT = """Generate comprehensive implementation details for this task:
Task: {task_name}
Module: {module_name}
Project Type: {project_type}
Language: {language}

Provide detailed task information including:
1. Clear goals and requirements
2. Step-by-step implementation approach
3. Specific subtasks (follow TDD - test first, then implementation)
4. Dependencies and prerequisites
5. Acceptance criteria
6. Potential challenges and solutions
7. Code quality considerations
8. Any necessary research or learning topics

Return a detailed task specification as a JSON object."""

MODULE_DOCUMENTATION_ENHANCEMENT_PROMPT = """Enhance the documentation for this module:
Module: {module_name}
Current Description: {description}
Project Type: {project_type}
Language: {language}
Other Modules: {other_modules}

Create comprehensive documentation that includes:
1. Detailed purpose and responsibilities
2. Key components and their roles
3. API design (if applicable)
4. Internal architecture
5. Dependencies and interactions with other modules
6. Data flow and state management
7. Error handling approach
8. Performance considerations
9. Security considerations
10. Testing approach
11. Example usage patterns
12. Extension points

Return the enhanced documentation as a structured JSON object."""

MODULE_DOCUMENTATION_REFINEMENT_PROMPT = """Current module documentation:
{current_doc}

User feedback: {feedback}

Refine the module documentation based on the feedback. Maintain all the good aspects while addressing the specific concerns raised.
Return the updated documentation in the same JSON structure."""

GLOBAL_RULES_GENERATION_PROMPT = """Based on this project configuration:
{config}

Generate 10-15 specific coding rules and best practices for this project.
Consider:
1. Language-specific best practices ({language})
2. Project type conventions ({project_type})
3. Code organization and structure
4. Naming conventions
5. Error handling patterns
6. Security practices
7. Performance guidelines
8. Testing requirements
9. Documentation standards
10. Git commit conventions
11. Dependency management
12. API design (if applicable)
13. Database patterns (if applicable)
14. Frontend practices (if applicable)
15. Architecture patterns

Return as a JSON array of rule strings, each being specific and actionable."""

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

MODULE_DESCRIPTION_BATCH_PROMPT = """Generate concise descriptions for these modules in a {project_type} project ({language}):

{modules_list}

Project context: {project_description}

For each module, provide a one-line description (max 100 chars) that clearly states its purpose.
Return as JSON: {{"module_name": "description", ...}}"""

TASK_DETAILS_BATCH_PROMPT = """Generate implementation details for these tasks:
{tasks_json}

Project Type: {project_type}
Language: {language}

For EACH task, provide:
1. Implementation approach (2-3 sentences)
2. Key subtasks (3-5 items, following TDD)
3. Main acceptance criteria (2-3 items)
4. Primary dependencies

Keep each task detail concise but comprehensive.
Return as JSON: {{
    "task_name": {{
        "approach": "...",
        "subtasks": ["Test: ...", "Implement: ...", ...],
        "acceptance_criteria": ["...", ...],
        "dependencies": ["...", ...]
    }},
    ...
}}"""

# Q&A and Discovery Prompts

PROJECT_QUESTIONS_INITIAL_PROMPT = """You are an expert software architect conducting a discovery session for a new project.

Project Description: "{project_description}"

Generate a single, highly relevant question to understand this project better. The question should:
- Be specific and require a detailed answer
- Focus on one aspect at a time
- Help clarify requirements, constraints, or implementation details
- Be appropriate for the project type

Categories to explore: {categories}

Output format:
{{
    "question": "Your specific question here",
    "category": "One of: {categories}",
    "importance": "high/medium/low",
    "reason": "Why this information is important"
}}"""

PROJECT_QUESTIONS_CONTEXTUAL_PROMPT = """You are conducting a detailed discovery session for a software project. Your goal is to understand ALL aspects needed to develop this project successfully.

Project Description: "{project_description}"
{qa_context}

Based on the project description and any previous Q&A above, generate the NEXT SINGLE most important question to ask.

The question should explore one of these aspects (choose what's most needed based on context):
1. **Technical Stack**: Specific technologies, frameworks, libraries, or tools
2. **Architecture**: System design, microservices vs monolith, API structure, database design
3. **Features**: Detailed functionality, user stories, edge cases, priority features
4. **UI/UX**: Design requirements, responsive needs, accessibility, user flow
5. **Authentication**: User management, roles, permissions, security requirements
6. **Data Model**: Entities, relationships, data flow, storage requirements
7. **API Design**: Endpoints, data formats, versioning, rate limiting
8. **Integrations**: Third-party services, external APIs, webhooks
9. **Performance**: Expected load, optimization needs, caching strategy
10. **Security**: Data protection, compliance requirements, threat model
11. **Deployment**: Hosting preferences, CI/CD, environments, scaling needs
12. **Timeline**: Deadlines, phases, MVP vs full product
13. **Testing**: Testing strategy, coverage requirements, automation needs
14. **Error Handling**: Logging, monitoring, alerting, recovery strategies
15. **Documentation**: Documentation needs, API docs, user guides
16. **Future Extensibility**: Planned features, scalability considerations

Rules for question generation:
- Ask about something NOT already covered in previous Q&A
- Be specific and require detailed answers (not just yes/no)
- Focus on information that would directly impact development decisions
- Prioritize critical information over nice-to-have details
- If you've covered most technical aspects, explore constraints, timeline, or specific requirements

Output format:
{{
    "question": "Your specific question here",
    "category": "Category name from the list above",
    "importance": "high/medium/low",
    "reason": "Why this information is important for development"
}}"""

QA_COMPILATION_TO_SPEC_PROMPT = """
Based on this initial project description: "{project_description}"

And this comprehensive Q&A session that explored the project in detail:
{qa_text}

Create a detailed technical specification that synthesizes all the information gathered.
The specification should be coherent and well-structured, incorporating insights from the entire conversation.

Include the following sections:

1. **Project Overview**: Clear, enhanced summary based on all Q&A insights
2. **Technical Stack**: Complete list of technologies, languages, frameworks, and tools discussed
3. **Core Features**: Comprehensive feature list with descriptions from Q&A
4. **Architecture Overview**: System design incorporating architectural decisions discussed
5. **Data Model**: Database schema and data flow based on requirements gathered
6. **API Design**: Endpoints, authentication, and integration points mentioned
7. **User Interface**: UI/UX requirements and design principles discussed
8. **Deployment Strategy**: Hosting, CI/CD, and infrastructure based on Q&A
9. **Security Considerations**: All security aspects mentioned in the conversation
10. **Performance Requirements**: Load expectations and optimization needs discussed
11. **Integration Requirements**: Third-party services and APIs from Q&A
12. **Development Constraints**: Timeline, budget, and limitations mentioned
13. **Testing Strategy**: Testing approach based on project requirements
14. **Future Considerations**: Scalability and future features discussed

Make sure to:
- Reference specific answers from the Q&A when relevant
- Resolve any contradictions by using the most recent answers
- Fill in reasonable defaults for standard practices if not explicitly discussed
- Create a cohesive document that reads well as a complete specification

Format as a professional technical specification document.
"""

# Interactive Enhancement Prompts

DESCRIPTION_ENHANCEMENT_PROMPT = """Current project description: {description}

Enhance this description to be more comprehensive and clear. Include:
1. What the project does (main functionality)
2. Who it's for (target audience)
3. Key features and benefits
4. Technology highlights
5. What makes it unique or valuable

Keep it concise but informative (2-4 sentences). Return only the enhanced description text."""

MODULE_SUGGESTIONS_PROMPT = """Suggest modules for this project:
Type: {project_type}
Description: {description}
Language: {language}

Provide 5-10 well-structured modules that follow best practices for {language} and {project_type} projects.
Consider separation of concerns, single responsibility, and scalability.

Return as a simple JSON array of module names (lowercase, underscores for spaces).
Example: ["user_auth", "database", "api_handlers"]"""

MODULE_DESCRIPTION_PROMPT = """Provide a clear, concise description for the '{module_name}' module in a {project_type} project.
This module should handle {module_name} functionality.

Return just the description (one sentence, max 80 characters)."""

TASK_SUGGESTIONS_PROMPT = """Suggest development tasks for this project:
Type: {project_type}
Description: {description}
Language: {language}
Modules: {modules}

Provide 10-15 specific development tasks that would be needed to build this project.
Tasks should be:
- Specific and actionable
- Appropriately sized (not too large)
- Cover setup, implementation, testing, and deployment
- Follow a logical development order

Return as a JSON array of task names.
Example: ["Setup project structure", "Create user model", "Implement authentication"]"""

MODULE_ASSIGNMENT_PROMPT = """Which module should handle this task?
Task: {task}
Available modules: {modules}

Return just the module name that best fits this task."""

RULE_SUGGESTIONS_PROMPT = """Suggest coding rules and best practices for:
Project type: {project_type}
Language: {language}
Description: {description}

Provide 12-15 specific rules covering:
- Code style and formatting
- Architecture patterns
- Security practices
- Testing requirements
- Documentation standards
- Performance guidelines

Return as a JSON array of rule strings."""

TECHNICAL_CONSTRAINTS_PROMPT = """Based on this project:
Type: {project_type}
Language: {language}
Description: {description}

What are the likely technical constraints and requirements?
Consider: dependencies, versions, deployment needs, performance requirements, etc.

Return as a JSON object with constraint categories and their requirements."""

BUILD_COMMANDS_PROMPT = """Suggest appropriate build commands for:
Project type: {project_type}
Language: {language}

Provide standard commands for:
- install: Install dependencies
- test: Run tests
- build: Build for production
- dev: Start development server
- lint: Run linter

Return as a JSON object with command names as keys and command strings as values.
Use typical commands for {language} projects."""

# Configuration Enhancement Prompts

CONFIGURATION_REFINEMENT_PROMPT = """The user has requested the following improvements to the project configuration:

"{refinement_request}"

Current configuration summary:
- Project: {project_name}
- Type: {project_type}
- Modules: {modules}
- Tasks: {tasks_count} tasks defined

Please provide specific enhancements addressing the user's feedback.
Return as JSON with any updates to modules, tasks, rules, or other configuration."""

# Refinement Prompts

TEXT_REFINEMENT_PROMPT = """Current value: {current_value}

User feedback: {feedback}

Provide an improved version based on the feedback. Return only the refined text."""

LIST_REFINEMENT_PROMPT = """Current items:
{current_items}

User feedback: {feedback}

Provide an improved list based on the feedback. Return as a JSON array."""

DICT_REFINEMENT_PROMPT = """Current data:
{current_data}

User feedback: {feedback}

Provide improved data based on the feedback. Return as a JSON object with the same structure."""