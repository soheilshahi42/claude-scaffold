"""Icon definitions for better UI/UX using Unicode box drawing and symbols."""

from typing import Dict


class Icons:
    """Unicode icons for terminal UI - compatible with all terminals."""
    
    # Status icons
    SUCCESS = "✓"      # Check mark
    ERROR = "✗"        # X mark
    WARNING = "!"      # Warning
    INFO = "i"         # Info
    QUESTION = "?"     # Question
    
    # Progress icons
    LOADING = "◌"      # Loading circle
    PROGRESS = "▸"     # Progress arrow
    COMPLETE = "●"     # Filled circle
    
    # Priority icons
    HIGH_PRIORITY = "▲"     # Up triangle (high)
    MEDIUM_PRIORITY = "■"   # Square (medium)
    LOW_PRIORITY = "▼"      # Down triangle (low)
    
    # Action icons
    ROBOT = "[AI]"     # AI/Robot
    THINKING = "..."   # Thinking
    ANALYZE = "◎"      # Analyze
    BUILD = "▧"        # Build
    TEST = "◈"         # Test
    DOCUMENT = "▤"     # Document
    FOLDER = "▦"       # Folder
    FILE = "▪"         # File
    CODE = "<>"        # Code
    
    # Navigation icons
    ARROW_RIGHT = "→"  # Right arrow
    ARROW_DOWN = "↓"   # Down arrow
    BULLET = "•"       # Bullet point
    CHEVRON = "›"      # Chevron right
    
    # Module/Task icons
    MODULE = "□"       # Module box
    TASK = "☐"         # Task checkbox
    RULE = "§"         # Rules section
    CONFIG = "⚙"       # Settings gear
    GIT = "⎇"          # Git branch
    
    # UI elements
    BOX_TOP_LEFT = "┌"
    BOX_TOP_RIGHT = "┐"
    BOX_BOTTOM_LEFT = "└"
    BOX_BOTTOM_RIGHT = "┘"
    BOX_HORIZONTAL = "─"
    BOX_VERTICAL = "│"
    BOX_CROSS = "┼"
    BOX_T_DOWN = "┬"
    BOX_T_UP = "┴"
    BOX_T_RIGHT = "├"
    BOX_T_LEFT = "┤"
    
    # Special icons
    STAR = "★"         # Star
    HEART = "♥"        # Heart
    LIGHTNING = "⚡"    # Lightning
    CLOCK = "◷"        # Clock
    PACKAGE = "◰"      # Package
    
    @classmethod
    def get_priority_icon(cls, priority: str) -> str:
        """Get icon for priority level."""
        priority_map = {
            'high': cls.HIGH_PRIORITY,
            'medium': cls.MEDIUM_PRIORITY,
            'low': cls.LOW_PRIORITY
        }
        return priority_map.get(priority.lower(), cls.BULLET)
    
    @classmethod
    def get_status_icon(cls, status: str) -> str:
        """Get icon for status."""
        status_map = {
            'success': cls.SUCCESS,
            'error': cls.ERROR,
            'warning': cls.WARNING,
            'info': cls.INFO,
            'loading': cls.LOADING,
            'complete': cls.COMPLETE
        }
        return status_map.get(status.lower(), cls.BULLET)
    
    @classmethod
    def format_header(cls, text: str, width: int = 60) -> str:
        """Format a header with box drawing characters."""
        padding = width - len(text) - 2
        left_pad = padding // 2
        right_pad = padding - left_pad
        
        lines = [
            f"{cls.BOX_TOP_LEFT}{cls.BOX_HORIZONTAL * width}{cls.BOX_TOP_RIGHT}",
            f"{cls.BOX_VERTICAL}{' ' * left_pad}{text}{' ' * right_pad}{cls.BOX_VERTICAL}",
            f"{cls.BOX_BOTTOM_LEFT}{cls.BOX_HORIZONTAL * width}{cls.BOX_BOTTOM_RIGHT}"
        ]
        return '\n'.join(lines)


# Convenience instance
icons = Icons()