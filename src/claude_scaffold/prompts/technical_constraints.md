You are identifying technical constraints and requirements for a new project.

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
{
    "runtime": {
        "language_version": "Minimum required version",
        "environment": "Required runtime environment",
        "platform": "OS/platform constraints"
    },
    "dependencies": {
        "core_libraries": ["lib:version", ...],
        "compatibility": "Version constraints",
        "licenses": "License requirements"
    },
    "performance": {
        "response_time": "Target latency",
        "concurrent_users": "Expected load",
        "data_volume": "Storage needs",
        "availability": "Uptime requirement"
    },
    "security": {
        "authentication": "Auth requirements",
        "encryption": "Data protection needs",
        "compliance": ["Standards to meet"],
        "vulnerabilities": "Security considerations"
    },
    "infrastructure": {
        "hosting": "Deployment platform",
        "database": "Data storage needs",
        "caching": "Performance optimization",
        "cdn": "Content delivery needs"
    },
    "integrations": {
        "external_apis": ["Required integrations"],
        "data_formats": ["Supported formats"],
        "protocols": ["Communication protocols"]
    },
    "development": {
        "team_size": "Resource constraints",
        "expertise_required": ["Skill requirements"],
        "tooling": ["Development tools"],
        "timeline": "Time constraints"
    },
    "operations": {
        "monitoring": "Observability needs",
        "backup": "Data protection strategy",
        "support": "Maintenance requirements",
        "documentation": "Documentation needs"
    }
}

**CONSIDER {project_type} SPECIFICS:**
- Common {project_type} requirements
- Typical {project_type} constraints
- {project_type} best practices

**CONSIDER {language} SPECIFICS:**
- {language} ecosystem constraints
- Common {language} deployment patterns
- {language} performance characteristics