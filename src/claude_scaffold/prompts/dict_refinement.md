# Dictionary Refinement Prompt

## Description

This prompt refines structured data (dictionaries/objects) based on user feedback. It modifies fields, adds missing information, and improves data quality while maintaining the same JSON schema.

## Purpose

- Refine structured data based on feedback
- Add missing fields or enhance values
- Maintain JSON schema consistency
- Improve data quality and specificity
- Preserve essential information

## Prompt Content

```
You are refining structured data based on user feedback.

**CURRENT DATA:**
{current_data}

**USER FEEDBACK:**
{feedback}

**REFINEMENT APPROACH:**

1. **Understand the Feedback:**
   - Which fields need modification?
   - What improvements are requested?
   - Are there missing keys or values?

2. **Common Improvements:**
   - Add missing fields
   - Enhance existing values
   - Correct inaccuracies
   - Improve clarity and specificity
   - Remove unnecessary data

3. **Maintain Structure:**
   - Keep the same JSON schema
   - Preserve field types
   - Maintain relationships
   - Ensure consistency

**REFINEMENT RULES:**
- Address all points in the feedback
- Keep unchanged fields intact
- Improve overall data quality
- Ensure valid JSON output
- Preserve essential information

**OUTPUT FORMAT:**
Return a complete JSON object with the same structure but improved content based on the feedback.

**EXAMPLE:**
If feedback says "add more detail to descriptions", expand brief descriptions into comprehensive ones while maintaining the exact same JSON structure.
```