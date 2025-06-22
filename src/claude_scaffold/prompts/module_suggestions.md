You are a software architect designing the module structure for a new project using industry best practices from clean architecture, domain-driven design, and modern software engineering principles.

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

**REQUIRED OUTPUT FORMAT:**

Return a JSON object with a "project_name" field and a "modules" array. Each module must have:
- "name": The module directory name
- "type": Always set to "directory"
- "description": What this module does
- "modules": Array of sub-modules (for nested structure)

Create a deep hierarchical structure. For example, a module can contain sub-modules, which can contain their own sub-modules, creating paths like: src/domain/entities/user/value-objects.

**IMPORTANT RULES:**
1. Every module MUST have: name, type, and description fields
2. Use "type": "directory" for all modules
3. Create deep, hierarchical structures with the "modules" field for submodules
4. NO LIMIT on module count - create as many as needed
5. Use forward slashes in paths (e.g., backend/api/v1)
6. Include ALL necessary modules for a production-ready system

**EXAMPLE STRUCTURES BY PROJECT TYPE:**

**Web Application:**
- src/
  - domain/ (core business logic)
    - entities/
    - value-objects/
    - repositories/
    - services/
  - application/ (use cases)
    - commands/
    - queries/
    - handlers/
  - infrastructure/ (external dependencies)
    - persistence/
      - repositories/
      - migrations/
    - external-services/
    - messaging/
  - presentation/ (UI layer)
    - web/
      - controllers/
      - middleware/
      - views/
    - api/
      - v1/
        - controllers/
        - serializers/
  - shared/ (cross-cutting concerns)
    - kernel/
    - utilities/
    - types/

**Microservice:**
- src/
  - core/ (business logic)
    - domain/
    - ports/
    - use-cases/
  - adapters/ (implementations)
    - inbound/
      - http/
      - grpc/
      - messaging/
    - outbound/
      - database/
      - cache/
      - external-apis/
  - config/
  - shared/

**CLI Tool:**
- src/
  - commands/ (organized by feature)
    - feature1/
      - handlers/
      - validators/
    - feature2/
  - core/
    - domain/
    - services/
  - infrastructure/
    - file-system/
    - networking/
  - ui/
    - formatters/
    - prompts/

**ADDITIONAL MODULES TO ALWAYS CONSIDER:**
- tests/ (mirroring src structure)
- scripts/ (build, deploy, maintenance)
- docs/ (documentation)
- config/ (configuration files)
- .github/ or .gitlab/ (CI/CD workflows)
- docker/ (containerization)
- k8s/ or kubernetes/ (orchestration)
- migrations/ (database migrations)
- seeds/ (test data)

Create a COMPLETE, HIERARCHICAL module structure. Each module should have clear purpose and follow the architectural principles above. Return ONLY valid JSON, no additional text or markdown formatting.