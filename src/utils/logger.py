"""Centralized logging system for Claude Scaffold."""

import logging
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import os


class DebugLogger:
    """Enhanced logger with debug mode and detailed logging."""
    
    def __init__(self, debug_mode: bool = False, log_file: Optional[Path] = None):
        self.debug_mode = debug_mode or os.getenv('CLAUDE_SCAFFOLD_DEBUG', '').lower() in ['true', '1', 'yes']
        self.log_file = log_file or Path.home() / '.claude-scaffold' / 'debug.log'
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Set up logger
        self.logger = logging.getLogger('claude_scaffold')
        self.logger.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if self.debug_mode else logging.WARNING)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s' if self.debug_mode else '%(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - [%(session_id)s] - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Start session
        self.log_session_start()
    
    def log_session_start(self):
        """Log the start of a new session."""
        self.logger.info(
            "\n" + "=" * 80 + "\n" +
            f"Session started: {self.session_id}\n" +
            f"Debug mode: {self.debug_mode}\n" +
            f"Log file: {self.log_file}\n" +
            "=" * 80,
            extra={'session_id': self.session_id}
        )
    
    def debug(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log debug message with optional data."""
        if data:
            message = f"{message}\nData: {json.dumps(data, indent=2, default=str)}"
        self.logger.debug(message, extra={'session_id': self.session_id})
    
    def info(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log info message with optional data."""
        if data:
            message = f"{message}\nData: {json.dumps(data, indent=2, default=str)}"
        self.logger.info(message, extra={'session_id': self.session_id})
    
    def warning(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log warning message with optional data."""
        if data:
            message = f"{message}\nData: {json.dumps(data, indent=2, default=str)}"
        self.logger.warning(message, extra={'session_id': self.session_id})
    
    def error(self, message: str, error: Optional[Exception] = None, data: Optional[Dict[str, Any]] = None):
        """Log error message with exception details."""
        error_data = {}
        if error:
            error_data['error_type'] = type(error).__name__
            error_data['error_message'] = str(error)
            error_data['error_args'] = error.args if hasattr(error, 'args') else None
        
        if data:
            error_data.update(data)
        
        if error_data:
            message = f"{message}\nError details: {json.dumps(error_data, indent=2, default=str)}"
        
        self.logger.error(message, exc_info=error is not None, extra={'session_id': self.session_id})
    
    def log_claude_interaction(self, prompt: str, response: Optional[str] = None, 
                              error: Optional[Exception] = None, command: Optional[list] = None):
        """Log Claude CLI interactions for debugging."""
        interaction_data = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt[:500] + '...' if len(prompt) > 500 else prompt,
            'command': command,
            'response_length': len(response) if response else 0,
            'response_preview': response[:200] + '...' if response and len(response) > 200 else response,
            'error': str(error) if error else None
        }
        
        if error:
            self.error("Claude interaction failed", error, interaction_data)
        else:
            self.debug("Claude interaction", interaction_data)
    
    def log_json_parse_error(self, raw_text: str, error: Exception):
        """Log JSON parsing errors with context."""
        lines = raw_text.split('\n')
        preview_lines = 10
        
        error_data = {
            'raw_text_length': len(raw_text),
            'first_lines': lines[:preview_lines],
            'last_lines': lines[-preview_lines:] if len(lines) > preview_lines else [],
            'total_lines': len(lines),
            'error_message': str(error)
        }
        
        self.error("JSON parsing failed", error, error_data)
    
    def get_log_file_path(self) -> Path:
        """Get the current log file path."""
        return self.log_file
    
    def enable_debug_mode(self):
        """Enable debug mode at runtime."""
        self.debug_mode = True
        self.logger.setLevel(logging.DEBUG)
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.DEBUG)
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s'
                ))
        self.info("Debug mode enabled")
    
    def disable_debug_mode(self):
        """Disable debug mode at runtime."""
        self.debug_mode = False
        self.logger.setLevel(logging.INFO)
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.WARNING)
                handler.setFormatter(logging.Formatter('%(message)s'))
        self.info("Debug mode disabled")


# Global logger instance
_logger: Optional[DebugLogger] = None


def get_logger(debug_mode: Optional[bool] = None) -> DebugLogger:
    """Get or create the global logger instance."""
    global _logger
    
    if _logger is None:
        _logger = DebugLogger(debug_mode=debug_mode)
    elif debug_mode is not None and debug_mode != _logger.debug_mode:
        # Update debug mode if explicitly requested
        if debug_mode:
            _logger.enable_debug_mode()
        else:
            _logger.disable_debug_mode()
    
    return _logger