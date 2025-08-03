"""
Logging utility for Pinterest Automation Bot
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional

def setup_logger(name: str, log_file: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """Set up a logger with both file and console handlers."""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Rotating file handler (10MB max, keep 5 files)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get an existing logger by name."""
    return logging.getLogger(name)

class PinterestBotLogger:
    """Custom logger class for Pinterest Bot with additional functionality."""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.logger = setup_logger(name, log_file)
        self.performance_logs = []
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    
    def log_performance(self, operation: str, duration: float, success: bool = True):
        """Log performance metrics."""
        status = "SUCCESS" if success else "FAILED"
        message = f"PERFORMANCE - {operation}: {duration:.2f}s - {status}"
        self.logger.info(message)
        
        # Store for analytics
        self.performance_logs.append({
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'duration': duration,
            'success': success
        })
    
    def log_api_call(self, service: str, endpoint: str, status_code: int, duration: float):
        """Log API calls."""
        message = f"API - {service} {endpoint}: {status_code} ({duration:.2f}s)"
        if status_code >= 400:
            self.logger.error(message)
        else:
            self.logger.info(message)
    
    def log_content_generation(self, niche: str, theme: str, success: bool):
        """Log content generation events."""
        status = "SUCCESS" if success else "FAILED"
        message = f"CONTENT - Generated {niche}/{theme}: {status}"
        self.logger.info(message)
    
    def log_pin_creation(self, pin_id: str, board: str, success: bool):
        """Log Pinterest pin creation."""
        status = "SUCCESS" if success else "FAILED"
        message = f"PIN - Created {pin_id} on {board}: {status}"
        self.logger.info(message)
    
    def get_performance_summary(self) -> dict:
        """Get performance summary from logs."""
        if not self.performance_logs:
            return {}
        
        successful_ops = [log for log in self.performance_logs if log['success']]
        failed_ops = [log for log in self.performance_logs if not log['success']]
        
        return {
            'total_operations': len(self.performance_logs),
            'successful_operations': len(successful_ops),
            'failed_operations': len(failed_ops),
            'success_rate': len(successful_ops) / len(self.performance_logs) * 100,
            'avg_duration': sum(log['duration'] for log in self.performance_logs) / len(self.performance_logs)
        }