"""
Prompt loader for loading prompts from markdown files.

This module provides functionality to load prompt templates from markdown files
stored in the prompts directory, enabling easy modification and version control
of prompts without changing code.
"""

import os
from pathlib import Path
from typing import Dict, Optional


class PromptLoader:
    """Loads prompts from markdown files."""
    
    def __init__(self, prompts_dir: Optional[Path] = None):
        """Initialize the prompt loader.
        
        Args:
            prompts_dir: Directory containing prompt markdown files.
                        Defaults to ../prompts relative to this file.
        """
        if prompts_dir is None:
            # Default to the prompts directory relative to this file
            self.prompts_dir = Path(__file__).parent.parent / "prompts"
        else:
            self.prompts_dir = Path(prompts_dir)
            
        self._cache: Dict[str, str] = {}
        
    def load_prompt(self, prompt_name: str) -> str:
        """Load a prompt from a markdown file.
        
        Args:
            prompt_name: Name of the prompt file (without .md extension)
            
        Returns:
            The prompt content as a string
            
        Raises:
            FileNotFoundError: If the prompt file doesn't exist
            ValueError: If the prompt file is empty
        """
        # Check cache first
        if prompt_name in self._cache:
            return self._cache[prompt_name]
            
        # Construct file path
        file_path = self.prompts_dir / f"{prompt_name}.md"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
            
        # Read the file content
        content = file_path.read_text(encoding='utf-8').strip()
        
        if not content:
            raise ValueError(f"Prompt file is empty: {file_path}")
            
        # Cache the content
        self._cache[prompt_name] = content
        
        return content
        
    def reload_prompt(self, prompt_name: str) -> str:
        """Reload a prompt from disk, bypassing the cache.
        
        Args:
            prompt_name: Name of the prompt file (without .md extension)
            
        Returns:
            The prompt content as a string
        """
        # Remove from cache if present
        self._cache.pop(prompt_name, None)
        
        # Load fresh from disk
        return self.load_prompt(prompt_name)
        
    def list_prompts(self) -> list[str]:
        """List all available prompt names.
        
        Returns:
            List of prompt names (without .md extension)
        """
        if not self.prompts_dir.exists():
            return []
            
        prompts = []
        for file_path in self.prompts_dir.glob("*.md"):
            if file_path.name != "README.md":
                prompts.append(file_path.stem)
                
        return sorted(prompts)


# Global instance for convenience
_default_loader = None


def get_prompt(prompt_name: str) -> str:
    """Get a prompt using the default loader.
    
    Args:
        prompt_name: Name of the prompt file (without .md extension)
        
    Returns:
        The prompt content as a string
    """
    global _default_loader
    if _default_loader is None:
        _default_loader = PromptLoader()
    return _default_loader.load_prompt(prompt_name)