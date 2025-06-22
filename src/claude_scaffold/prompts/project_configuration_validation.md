# Project Configuration Validation Prompt

## Description

This prompt validates and enhances project configurations by reviewing them for completeness and best practices. It analyzes the configuration structure, identifies missing sections, and provides specific improvements while ensuring architectural soundness.

## Purpose

- Validate project configurations for completeness
- Identify missing or incomplete sections
- Provide specific improvement suggestions
- Assess architectural decisions and risks
- Return enhanced configurations with improvements

## Prompt Content

```
Review this project configuration for completeness and best practices:
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

Return a JSON object with your analysis and the enhanced configuration.
```