"""
Logger utility.
Non-compliant: no actual logging, just print statements.
"""
import sys
from datetime import datetime

class Logger:
    """Simple logger - no proper logging framework"""
    
    @staticmethod
    def info(message: str):
        """Log info - just prints"""
        print(f"[INFO] {datetime.now()} - {message}", file=sys.stdout)
    
    @staticmethod
    def error(message: str):
        """Log error - just prints"""
        print(f"[ERROR] {datetime.now()} - {message}", file=sys.stderr)
    
    @staticmethod
    def warning(message: str):
        """Log warning - just prints"""
        print(f"[WARNING] {datetime.now()} - {message}", file=sys.stdout)
    
    @staticmethod
    def debug(message: str):
        """Log debug - just prints"""
        print(f"[DEBUG] {datetime.now()} - {message}", file=sys.stdout)

