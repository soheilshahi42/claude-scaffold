# Q&A Compilation to Specification Prompt

## Description

This prompt synthesizes all information gathered during a discovery session into a comprehensive technical specification. It transforms Q&A transcripts into a professional, structured document that serves as the definitive guide for the development team.

## Purpose

- Convert discovery session Q&A into technical specifications
- Create comprehensive project documentation
- Ensure all requirements are captured and organized
- Provide clear implementation guidance
- Establish project constraints and timelines

## Prompt Content

```
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
```