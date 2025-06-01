"""Claude integration module - backward compatibility wrapper."""

# Re-export everything from the new modules for backward compatibility
from .claude_processor import ClaudeProcessor
from .claude_enhancer import ClaudeEnhancedSetup

__all__ = ['ClaudeProcessor', 'ClaudeEnhancedSetup']