"""
Prompts for interactive Q&A collection.

This module contains prompts used for the deep-dive Q&A discovery sessions.
"""

# Q&A Discovery Prompts

CONTEXTUAL_QUESTION_GENERATION_PROMPT = """You are conducting a detailed discovery session for a software project. Your goal is to understand ALL aspects needed to develop this project successfully.

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

# QA Collector specific prompt that returns in CATEGORY: question format
QA_COLLECTOR_QUESTION_PROMPT = """You are conducting a detailed discovery session for a software project. Your goal is to understand ALL aspects needed to develop this project successfully.

Project Description: "{project_description}"
{qa_context}

Based on the project description and any previous Q&A above, generate the NEXT SINGLE most important question to ask.

Consider these aspects that need to be covered throughout the session:
- Technical stack (languages, frameworks, databases, tools)
- Architecture and system design
- Core features and functionality
- User interface and user experience
- Authentication and authorization
- Data models and relationships
- API design and endpoints
- Third-party integrations
- Performance and scalability requirements
- Security considerations
- Deployment and hosting
- Development timeline and constraints
- Testing strategy
- Error handling and logging
- Documentation needs
- Future extensibility

Questions asked so far: {question_number}

Generate exactly ONE question that:
1. Builds on previous answers (if any)
2. Explores an aspect not yet covered
3. Is specific and actionable
4. Helps clarify technical decisions

Format: CATEGORY: question text

Categories: TECHNICAL, FEATURES, ARCHITECTURE, DEPLOYMENT, USERS, CONSTRAINTS, INTEGRATIONS"""