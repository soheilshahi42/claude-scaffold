"""
Prompts for interactive Q&A collection.

This module loads prompts from markdown files for the deep-dive Q&A discovery sessions
to gather comprehensive project requirements through intelligent questioning.
"""

from ..claude.prompt_loader import get_prompt

# Q&A Discovery Prompts
CONTEXTUAL_QUESTION_GENERATION_PROMPT = get_prompt("contextual_question_generation")

# QA Collector specific prompt that returns in CATEGORY: question format
QA_COLLECTOR_QUESTION_PROMPT = get_prompt("qa_collector_question")