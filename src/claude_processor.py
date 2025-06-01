"""Core Claude processing functionality."""

import subprocess
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional


class ClaudeProcessor:
    """Process user inputs through Claude in headless mode."""
    
    def __init__(self):
        self.claude_executable = "claude"  # Assumes claude is in PATH
    
    def process_project_setup(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process project setup through Claude to generate intelligent configuration."""
        
        prompt = f"""You are helping set up a new {initial_data['metadata']['project_type_name']} project.

Project Information:
- Name: {initial_data['project_name']}
- Description: {initial_data['metadata']['description']}
- Type: {initial_data['metadata']['project_type_name']}
- Language: {initial_data['metadata']['language']}

Based on this information, provide a comprehensive project configuration including:

1. Enhanced project description (2-3 sentences)
2. Detailed module responsibilities for each module:
{self._format_modules(initial_data['modules'])}

3. Task implementation details for each task:
{self._format_tasks(initial_data['tasks'])}

4. Additional project-specific rules (3-5 rules beyond the provided ones)
5. Architecture recommendations
6. Testing strategy recommendations
7. Security considerations
8. Performance optimization guidelines

Current Rules:
{self._format_rules(initial_data['rules'])}

Please return a JSON object with this enhanced configuration. Format:
{{
    "enhanced_description": "...",
    "module_enhancements": {{"module_name": {{...}}, ...}},
    "task_details": {{"task_title": {{...}}, ...}}, 
    "additional_rules": [...],
    "architecture_recommendations": {{...}},
    "testing_strategy": {{...}},
    "security_considerations": [...],
    "performance_guidelines": [...]
}}"""

        response = self._call_claude(prompt)
        claude_config = json.loads(response)
        
        # Merge Claude's enhancements with original data
        enhanced_data = self._merge_claude_config(initial_data, claude_config)
        
        return enhanced_data
    
    def generate_task_details(self, task_title: str, module_name: str, project_context: Dict) -> Dict[str, Any]:
        """Generate detailed task specifications using Claude."""
        
        prompt = f"""Generate comprehensive task details for the following task:

Task: {task_title}
Module: {module_name}
Project Type: {project_context['metadata']['project_type_name']}
Project Description: {project_context['metadata']['description']}

Please provide:
1. Clear goal statement
2. Key requirements (3-5 items)
3. Recommended implementation approach
4. Specific subtasks following TDD methodology (5-8 items)
5. Acceptance criteria
6. Potential challenges
7. Research topics

Return as JSON with keys: goal, requirements, approach, subtasks, acceptance_criteria, challenges, research_topics"""

        response = self._call_claude(prompt)
        return json.loads(response)
    
    def enhance_module_documentation(self, module: Dict, project_context: Dict) -> Dict[str, Any]:
        """Generate enhanced module documentation using Claude."""
        
        prompt = f"""Generate comprehensive documentation for the following module:

Module: {module['name']}
Description: {module['description']}
Project Type: {project_context['metadata']['project_type_name']}

Please provide:
1. Detailed responsibilities (paragraph format)
2. Public API design suggestions
3. Internal architecture recommendations
4. Key dependencies with purposes
5. Interaction patterns with other modules
6. Error handling strategies
7. Performance considerations
8. Security considerations
9. Usage examples

Return as JSON."""

        response = self._call_claude(prompt)
        return json.loads(response)
    
    def generate_global_rules(self, project_data: Dict) -> List[str]:
        """Generate project-specific global rules using Claude."""
        
        prompt = f"""Generate 10-15 project-specific rules for a {project_data['metadata']['project_type_name']} project.

Project: {project_data['project_name']}
Description: {project_data['metadata']['description']}
Language: {project_data['metadata']['language']}
Modules: {', '.join(m['name'] for m in project_data['modules'])}

Consider:
- Best practices for {project_data['metadata']['project_type_name']} projects
- {project_data['metadata']['language']} specific conventions
- Security and performance requirements
- Testing and documentation standards
- Code organization and architecture

Existing rules to complement (don't repeat these):
{self._format_list(project_data['rules']['suggested'] + project_data['rules']['custom'])}

Return as JSON array of rule strings."""

        response = self._call_claude(prompt)
        return json.loads(response)
    
    def validate_project_configuration(self, project_data: Dict) -> Dict[str, Any]:
        """Validate and suggest improvements for project configuration."""
        
        prompt = f"""Review and validate this project configuration:

{json.dumps(project_data, indent=2)}

Please analyze:
1. Are all modules necessary and well-defined?
2. Are tasks properly distributed across modules?
3. Are there any missing critical components?
4. Are the rules comprehensive and consistent?
5. Any architectural concerns?

Return JSON with:
{{
    "is_valid": true/false,
    "suggestions": [...],
    "missing_components": [...],
    "architectural_concerns": [...],
    "overall_assessment": "..."
}}"""

        response = self._call_claude(prompt)
        return json.loads(response)
    
    def _call_claude(self, prompt: str, timeout: int = 60) -> str:
        """Call Claude in headless mode with a prompt."""
        # Create temporary file for prompt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(prompt)
            prompt_file = f.name
        
        try:
            # Call Claude with the prompt file
            cmd = [
                self.claude_executable,
                '--max-tokens', '4000',
                prompt_file
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Claude returned error: {result.stderr}")
            
            return result.stdout.strip()
            
        finally:
            # Clean up temp file
            Path(prompt_file).unlink(missing_ok=True)
    
    def _merge_claude_config(self, original_data: Dict, claude_config: Dict) -> Dict[str, Any]:
        """Merge Claude's enhancements with original data."""
        enhanced_data = original_data.copy()
        
        # Update description
        if 'enhanced_description' in claude_config:
            enhanced_data['metadata']['description'] = claude_config['enhanced_description']
        
        # Enhance modules
        if 'module_enhancements' in claude_config:
            for module in enhanced_data['modules']:
                if module['name'] in claude_config['module_enhancements']:
                    module['documentation'] = claude_config['module_enhancements'][module['name']]
        
        # Enhance tasks
        if 'task_details' in claude_config:
            for task in enhanced_data['tasks']:
                if task['title'] in claude_config['task_details']:
                    task['details'] = claude_config['task_details'][task['title']]
        
        # Add additional rules
        if 'additional_rules' in claude_config:
            enhanced_data['rules']['suggested'].extend(claude_config['additional_rules'])
        
        # Add other enhancements
        for key in ['architecture_recommendations', 'testing_strategy', 
                   'security_considerations', 'performance_guidelines']:
            if key in claude_config:
                enhanced_data['metadata'][key] = claude_config[key]
        
        return enhanced_data
    
    def _format_modules(self, modules: List[Dict]) -> str:
        """Format modules for prompt."""
        return '\n'.join([f"- {m['name']}: {m['description']}" for m in modules])
    
    def _format_tasks(self, tasks: List[Dict]) -> str:
        """Format tasks for prompt."""
        return '\n'.join([f"- [{t['module']}] {t['title']} (Priority: {t['priority']})" for t in tasks])
    
    def _format_rules(self, rules: Dict) -> str:
        """Format rules for prompt."""
        all_rules = rules.get('suggested', []) + rules.get('custom', [])
        if not all_rules:
            return "No existing rules"
        return '\n'.join([f"- {rule}" for rule in all_rules])
    
    def _format_list(self, items: List[str]) -> str:
        """Format a list for prompt."""
        if not items:
            return "None"
        return '\n'.join([f"- {item}" for item in items])