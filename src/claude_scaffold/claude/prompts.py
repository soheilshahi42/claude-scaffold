"""
Prompts for Claude API interactions.

This module loads all prompts from markdown files in the prompts directory,
enabling easy modification and version control of prompts without changing code.
"""

from .prompt_loader import get_prompt

# Project Setup and Configuration Prompts
PROJECT_SETUP_ENHANCEMENT_PROMPT = get_prompt("project_setup_enhancement")
TASK_DETAILS_GENERATION_PROMPT = get_prompt("task_details_generation")
MODULE_DOCUMENTATION_ENHANCEMENT_PROMPT = get_prompt("module_documentation_enhancement")
MODULE_DOCUMENTATION_REFINEMENT_PROMPT = get_prompt("module_documentation_refinement")
GLOBAL_RULES_GENERATION_PROMPT = get_prompt("global_rules_generation")
PROJECT_CONFIGURATION_VALIDATION_PROMPT = get_prompt("project_configuration_validation")
MODULE_DESCRIPTION_BATCH_PROMPT = get_prompt("module_description_batch")
TASK_DETAILS_BATCH_PROMPT = get_prompt("task_details_batch")

# Q&A Discovery Prompts
PROJECT_QUESTIONS_INITIAL_PROMPT = get_prompt("project_questions_initial")
PROJECT_QUESTIONS_CONTEXTUAL_PROMPT = get_prompt("project_questions_contextual")
QA_COMPILATION_TO_SPEC_PROMPT = get_prompt("qa_compilation_to_spec")

# Enhancement and Refinement Prompts
DESCRIPTION_ENHANCEMENT_PROMPT = get_prompt("description_enhancement")
MODULE_SUGGESTIONS_PROMPT = get_prompt("module_suggestions")
MODULE_DESCRIPTION_PROMPT = get_prompt("module_description")
TASK_SUGGESTIONS_PROMPT = get_prompt("task_suggestions")
MODULE_ASSIGNMENT_PROMPT = get_prompt("module_assignment")
RULE_SUGGESTIONS_PROMPT = get_prompt("rule_suggestions")

# Technical Setup Prompts
TECHNICAL_CONSTRAINTS_PROMPT = get_prompt("technical_constraints")
BUILD_COMMANDS_PROMPT = get_prompt("build_commands")
CONFIGURATION_REFINEMENT_PROMPT = get_prompt("configuration_refinement")

# Refinement Prompts
TEXT_REFINEMENT_PROMPT = get_prompt("text_refinement")
LIST_REFINEMENT_PROMPT = get_prompt("list_refinement")
DICT_REFINEMENT_PROMPT = get_prompt("dict_refinement")