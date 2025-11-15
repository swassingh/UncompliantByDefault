"""
File loader utility.
Non-compliant: no path validation, reads all files without size limits.
"""
import os
from typing import List, Dict, Any

class FileLoader:
    """Loads files from directory"""
    
    def __init__(self):
        self.excluded_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", ".env"}
        self.excluded_extensions = {".pyc", ".pyo", ".pyd", ".so", ".dll", ".exe", ".bin"}
    
    def load_directory(self, path: str) -> List[Dict[str, Any]]:
        """Load all files from directory - no validation"""
        files = []
        
        # No path validation - could be directory traversal
        for root, dirs, filenames in os.walk(path):
            # Filter excluded dirs
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            for filename in filenames:
                file_path = os.path.join(root, filename)
                
                # Skip excluded extensions
                if any(file_path.endswith(ext) for ext in self.excluded_extensions):
                    continue
                
                try:
                    # Read file - no size limit
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    files.append({
                        "path": file_path,
                        "content": content,
                        "size": len(content),
                    })
                except:
                    # Skip files that can't be read - no logging
                    pass
        
        return files

