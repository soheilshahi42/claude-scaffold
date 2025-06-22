# Description Enhancement Prompt

## Description

This prompt enhances project descriptions to be more professional, comprehensive, and compelling. It transforms basic descriptions into well-structured narratives that clearly communicate the project's value proposition, target audience, and key differentiators.

## Purpose

- Transform basic descriptions into professional narratives
- Clearly communicate project value and scope
- Identify target audience and use cases
- Highlight key technical approaches
- Create compelling project overviews

## Prompt Content

```
You are enhancing a project description to be more professional and comprehensive.

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
Return ONLY the enhanced description text, no additional commentary.
```