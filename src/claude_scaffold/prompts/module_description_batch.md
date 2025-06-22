You are creating concise, precise module descriptions for a development team.

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
{
    "module_name": "Clear, specific description under 100 chars",
    "module_name2": "Another description",
    ...
}

**CONTEXT-SPECIFIC GUIDANCE:**
For {project_type} projects in {language}, consider:
- Common patterns and responsibilities in {project_type} architecture
- {language}-specific conventions and frameworks
- How these modules typically interact in {project_type} systems