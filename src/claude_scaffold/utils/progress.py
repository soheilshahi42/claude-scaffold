"""Simple progress indicator stub to fix import errors."""

class DummyProgress:
    """Dummy progress class that does nothing."""
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass
    
    def update_status(self, *args, **kwargs):
        pass
    
    def set_prompt_size(self, *args):
        pass
    
    def update_task_batch(self, *args):
        pass
    
    def show_result(self, *args):
        pass


class ProgressIndicator:
    """Minimal progress indicator that doesn't break existing code."""
    
    def claude_thinking(self, message: str):
        """Return a dummy context manager."""
        print(f"🤖 {message}...")
        return DummyProgress()
    
    def show_retry(self, attempt: int, max_retries: int, wait_time: int):
        """Show retry message."""
        print(f"⚡ Retry {attempt}/{max_retries} after {wait_time}s")
    
    def show_error(self, message: str):
        """Show error message."""
        print(f"❌ {message}")


# Global instance
progress_indicator = ProgressIndicator()