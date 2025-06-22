# Text Refinement Prompt

## Description

This prompt refines text content based on specific user feedback. It analyzes the feedback type and improves the text while maintaining the original intent and appropriate constraints.

## Purpose

- Refine text based on user feedback
- Address clarity, specificity, and verbosity issues
- Maintain original intent and tone
- Fix issues while improving overall quality
- Return only the improved text

## Prompt Content

```
You are refining text based on specific user feedback.

**CURRENT TEXT:**
{current_value}

**USER FEEDBACK:**
{feedback}

**REFINEMENT GUIDELINES:**

1. **Analyze Feedback Type:**
   - Clarity issue → Simplify and clarify
   - Too generic → Add specifics and examples
   - Too verbose → Condense while keeping key info
   - Wrong focus → Shift emphasis appropriately
   - Missing info → Add requested details

2. **Maintain:**
   - Original intent and purpose
   - Appropriate tone and style
   - Any constraints (length, format)

3. **Improve:**
   - Address the specific issue raised
   - Enhance overall quality
   - Fix any other obvious issues

**OUTPUT:**
Return ONLY the improved text (no explanation or commentary).
```