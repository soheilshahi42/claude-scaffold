# Module Documentation Enhancement Prompt

## Description

This prompt creates comprehensive module documentation that serves as the definitive guide for a module within the system. It generates detailed documentation covering architecture, API, dependencies, configuration, error handling, performance, security, testing, and usage examples.

## Purpose

- Create detailed, actionable documentation for each module
- Define clear module boundaries and responsibilities
- Document public APIs and integration points
- Establish module-specific patterns and practices
- Provide comprehensive usage examples and extension guides

## Prompt Content

```
You are a technical architect creating comprehensive module documentation.

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
   {
       "purpose": "Clear statement of what this module does and why it exists",
       "scope": "What is included and explicitly excluded",
       "key_features": ["Feature 1", "Feature 2", ...]
   }

2. **Architecture** (architecture):
   {
       "design_pattern": "e.g., Repository, Service Layer, MVC",
       "components": [
           {
               "name": "ComponentName",
               "type": "class|interface|service|utility",
               "responsibility": "What it does",
               "location": "path/to/component.{ext}"
           }
       ],
       "data_flow": "How data moves through the module",
       "state_management": "How state is handled (if applicable)"
   }

3. **Public API** (public_api):
   {
       "endpoints": [
           {
               "name": "functionName",
               "description": "What it does",
               "parameters": [{"name": "param", "type": "string", "required": true, "description": "..."}],
               "returns": {"type": "Object", "description": "..."},
               "throws": [{"type": "ErrorType", "condition": "When..."}],
               "example": "Code example"
           }
       ],
       "events": [{"name": "eventName", "payload": {...}, "when": "..."}],
       "constants": [{"name": "CONSTANT_NAME", "value": "...", "description": "..."}]
   }

4. **Dependencies** (dependencies):
   {
       "internal_modules": [
           {"module": "module_name", "purpose": "Why we depend on it", "interfaces_used": [...]}
       ],
       "external_packages": [
           {"package": "package_name", "version": "^1.0.0", "purpose": "...", "alternatives": [...]}
       ],
       "system_requirements": ["Requirement 1", ...]
   }

5. **Configuration** (configuration):
   {
       "environment_variables": [
           {"name": "VAR_NAME", "type": "string", "default": "...", "description": "..."}
       ],
       "config_files": [{"path": "config/module.json", "format": "JSON", "schema": {...}}],
       "feature_flags": [{"name": "FEATURE_NAME", "default": false, "description": "..."}]
   }

6. **Error Handling** (error_handling):
   {
       "error_types": [
           {
               "name": "ValidationError",
               "when": "Input validation fails",
               "recovery": "How to handle",
               "user_message": "What users see"
           }
       ],
       "error_codes": [{"code": "MOD_001", "meaning": "...", "action": "..."}],
       "logging_strategy": "What gets logged and at what level"
   }

7. **Performance** (performance):
   {
       "optimization_strategies": ["Caching approach", "Query optimization", ...],
       "benchmarks": {"operation": "Expected time/throughput"},
       "resource_limits": {"memory": "Max MB", "cpu": "Max %", "connections": "Max concurrent"},
       "monitoring_points": ["What to monitor", ...]
   }

8. **Security** (security):
   {
       "authentication": "How authentication is handled",
       "authorization": "Permission model used",
       "data_validation": "Input sanitization approach",
       "sensitive_data": ["What data is sensitive and how it's protected"],
       "security_headers": ["Headers added by this module"],
       "rate_limiting": "If and how rate limiting is applied"
   }

9. **Testing** (testing):
   {
       "test_strategy": "Overall approach to testing this module",
       "test_categories": [
           {"type": "unit", "location": "tests/unit/module_name", "coverage_target": "90%"},
           {"type": "integration", "location": "tests/integration/module_name", "key_scenarios": [...]}
       ],
       "test_data": "How test data is managed",
       "mocking_strategy": "What gets mocked and how"
   }

10. **Usage Examples** (examples):
    [
        {
            "scenario": "Basic usage",
            "description": "How to perform common operation",
            "code": "// Complete code example\n// with proper error handling",
            "output": "Expected result"
        }
    ]

11. **Extension Guide** (extension_guide):
    {
        "extension_points": [
            {"name": "Custom validator", "interface": "IValidator", "how_to": "..."}
        ],
        "plugin_system": "If applicable, how to create plugins",
        "event_hooks": [{"event": "beforeSave", "purpose": "...", "example": "..."}]
    }

12. **Migration Guide** (migration):
    {
        "from_version": "Previous version migration notes",
        "breaking_changes": ["List of breaking changes"],
        "deprecations": [{"feature": "...", "replacement": "...", "removal_date": "..."}]
    }

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
✓ Testing strategy is actionable
```