"""Claude enhancement functionality for interactive setup."""

import json
import questionary
from typing import Dict, Any

from .claude_processor import ClaudeProcessor
from ..utils.progress import progress_indicator


class ClaudeEnhancedSetup:
    """Enhanced setup using Claude for intelligent configuration."""
    
    def __init__(self, interactive_setup, timeout: int = 300, max_retries: int = 3):
        self.interactive_setup = interactive_setup
        self.processor = ClaudeProcessor(timeout=timeout, max_retries=max_retries)
    
    def enhance_with_claude(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance project configuration using Claude."""
        print("\n" + "=" * 60)
        print("🤖 CLAUDE ENHANCEMENT")
        print("=" * 60)
        
        use_claude = questionary.confirm(
            "\n🤖 Would you like Claude to enhance your configuration with intelligent suggestions?",
            default=True
        ).ask()
        
        if not use_claude:
            return project_data
        
        return self.enhance_project_data(project_data)
    
    def enhance_project_data(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process project data through Claude for enhancements."""
        try:
            print("\n🤖 Consulting Claude for intelligent project configuration...")
            
            # Process the entire project setup
            enhanced_data = self.processor.process_project_setup(project_data)
            
            # Generate task details in batch
            tasks_needing_details = [task for task in enhanced_data['tasks'] if 'details' not in task]
            if tasks_needing_details:
                print("📝 Generating detailed task specifications...")
                task_details = self.processor.generate_task_details_batch(
                    tasks_needing_details,
                    enhanced_data
                )
                # Update tasks with details
                for task in enhanced_data['tasks']:
                    if task['title'] in task_details:
                        task['details'] = task_details[task['title']]
            
            # Enhance module documentation
            modules_needing_docs = [module for module in enhanced_data['modules'] if 'documentation' not in module]
            if modules_needing_docs:
                print("📚 Enhancing module documentation...")
                # For now, use individual calls for module documentation
                # as they require more complex processing
                for module in modules_needing_docs:
                    try:
                        module['documentation'] = self.processor.enhance_module_documentation(
                            module,
                            enhanced_data
                        )
                    except Exception as e:
                        self.processor.logger.warning(f"Failed to enhance module {module['name']}: {e}")
            
            # Generate additional global rules
            print("📏 Generating comprehensive project rules...")
            try:
                additional_rules = self.processor.generate_global_rules(enhanced_data)
                enhanced_data['rules']['suggested'].extend(additional_rules[:5])  # Add top 5 rules
            except Exception as e:
                self.processor.logger.warning(f"Failed to generate global rules: {e}")
            
            # Validate configuration
            print("✅ Validating project configuration...")
            try:
                validation = self.processor.validate_project_configuration(enhanced_data)
            except Exception as e:
                self.processor.logger.warning(f"Failed to validate configuration: {e}")
                validation = {"suggestions": []}
            
            if validation.get('suggestions'):
                print("\n💡 Claude suggests:")
                for suggestion in validation['suggestions'][:3]:
                    print(f"   • {suggestion}")
            
            # Interactive enhancement loop
            enhanced_data = self.interactive_enhancement_loop(enhanced_data)
            
            return enhanced_data
            
        except Exception as e:
            print(f"\n⚠️  Claude enhancement failed: {e}")
            print("   Continuing with standard configuration...")
            return project_data
    
    def interactive_enhancement_loop(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Allow user to refine configuration with Claude's help."""
        while True:
            # Show enhanced summary
            self._show_enhanced_summary(project_data)
            
            # Ask if configuration is perfect
            response = questionary.select(
                "\n🎯 Is this configuration perfect?",
                choices=['yes', 'no', 'modify']
            ).ask()
            
            if response == 'yes':
                break
            elif response == 'modify':
                # Allow manual modifications
                modification = questionary.text(
                    "What would you like to modify? (e.g., 'add task: Create API docs to api module')"
                ).ask()
                project_data = self._process_modification(project_data, modification)
            else:  # response == 'no'
                # Ask what needs improvement
                improvement = questionary.text(
                    "What aspects need improvement? (Claude will refine based on your feedback)"
                ).ask()
                project_data = self._refine_with_claude(project_data, improvement)
        
        return project_data
    
    def _show_enhanced_summary(self, data: Dict[str, Any]):
        """Show enhanced configuration summary."""
        print("\n" + "=" * 50)
        print("✨ CLAUDE-ENHANCED CONFIGURATION")
        print("=" * 50)
        
        print(f"\n📝 Enhanced Description:")
        print(f"   {data['metadata']['description']}")
        
        print(f"\n📦 Enhanced Modules:")
        for module in data['modules']:
            if 'documentation' in module:
                print(f"   • {module['name']}: {module['documentation'].get('responsibilities', module['description'])[:100]}...")
        
        print(f"\n📋 Enhanced Tasks:")
        for task in data['tasks'][:3]:
            if 'details' in task:
                print(f"   • {task['title']}")
                print(f"     Goal: {task['details'].get('goal', 'Not defined')[:80]}...")
        
        if len(data['tasks']) > 3:
            print(f"   ... and {len(data['tasks']) - 3} more tasks")
    
    def _process_modification(self, data: Dict, modification: str) -> Dict[str, Any]:
        """Process user modification request."""
        # Simple modification parser (can be enhanced)
        mod_lower = modification.lower()
        
        if 'add task:' in mod_lower:
            # Extract task details
            parts = modification.split(':', 1)[1].strip()
            if ' to ' in parts:
                task_title, module = parts.rsplit(' to ', 1)
                task_title = task_title.strip()
                module = module.strip()
                
                # Add the task
                data['tasks'].append({
                    'title': task_title,
                    'module': module,
                    'priority': 'medium',
                    'type': 'added'
                })
                print(f"✅ Added task '{task_title}' to module '{module}'")
        
        return data
    
    def _refine_with_claude(self, data: Dict, refinement_request: str) -> Dict[str, Any]:
        """Refine configuration based on user feedback."""
        print("\n🤖 Claude is refining the configuration based on your feedback...")
        
        # Create refinement prompt
        prompt = f"""The user has requested the following improvements to the project configuration:

"{refinement_request}"

Current configuration summary:
- Project: {data['project_name']}
- Type: {data['metadata']['project_type_name']}
- Modules: {', '.join(m['name'] for m in data['modules'])}
- Tasks: {len(data['tasks'])} tasks defined

Please provide specific enhancements addressing the user's feedback.
Return as JSON with any updates to modules, tasks, rules, or other configuration."""
        
        try:
            response = self.processor._call_claude(prompt)
            refinements = json.loads(response)
            
            # Apply refinements (simplified - can be enhanced)
            if 'modules' in refinements:
                data['modules'] = refinements['modules']
            if 'tasks' in refinements:
                data['tasks'].extend(refinements.get('new_tasks', []))
            
            print("✅ Configuration refined based on your feedback")
        except Exception as e:
            print(f"⚠️  Refinement failed: {e}")
        
        return data