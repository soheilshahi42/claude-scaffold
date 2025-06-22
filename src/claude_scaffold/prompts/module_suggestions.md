# Module Suggestions Prompt

## Description

This prompt generates comprehensive module structures for projects following industry best practices from clean architecture, domain-driven design, and modern software engineering principles. It creates hierarchical, feature-based module organizations tailored to the project type and language.

## Purpose

- Design comprehensive module structures for new projects
- Apply clean architecture and DDD principles
- Create feature-based organization with vertical slicing
- Ensure scalable and maintainable code structure
- Generate production-ready module hierarchies

## Prompt Content

```
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
- Technology-specific names in domain layer
```