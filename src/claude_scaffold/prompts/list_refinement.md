# List Refinement Prompt

## Description

This prompt refines lists based on user feedback. It analyzes feedback patterns to add, remove, or modify list items while maintaining quality principles and appropriate structure.

## Purpose

- Refine lists based on specific feedback
- Add, remove, or modify items as needed
- Maintain list quality and consistency
- Ensure appropriate length and ordering
- Return properly formatted JSON arrays

## Prompt Content

```
You are refining a list based on user feedback.

**CURRENT LIST:**
{current_items}

**USER FEEDBACK:**
{feedback}

**REFINEMENT STRATEGIES:**

1. **Common Feedback Patterns:**
   - "Too few" → Add more relevant items
   - "Too many" → Remove less important ones
   - "Wrong focus" → Replace with better alternatives
   - "Too generic" → Make items more specific
   - "Missing X" → Add the specific requested items

2. **List Quality Principles:**
   - Each item should be distinct and valuable
   - Order by importance or logical sequence
   - Consistent level of detail
   - No redundancy or overlap

3. **Improvement Process:**
   - Keep good items from original
   - Address specific feedback
   - Enhance overall quality
   - Maintain appropriate length

**OUTPUT FORMAT:**
Return a JSON array with improved items:
["item1", "item2", ...]

**ENSURE:**
- Valid JSON format
- Appropriate number of items
- Directly addresses feedback
- Maintains or improves quality
```