"""Configuration management utilities."""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ConfigManager:
    """Manages project configuration loading and saving."""
    
    @staticmethod
    def save_config(project_data: Dict[str, Any], path: Path) -> None:
        """Save project configuration to file."""
        config_path = path / ".claude" / "project_config.yaml"
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, "w") as f:
            yaml.dump(project_data, f, default_flow_style=False, sort_keys=False)
    
    @staticmethod
    def load_config(path: Path) -> Optional[Dict[str, Any]]:
        """Load project configuration from file."""
        config_path = path / ".claude" / "project_config.yaml"
        
        if not config_path.exists():
            return None
            
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception:
            return None