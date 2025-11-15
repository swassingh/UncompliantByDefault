"""
GitHub repository loader.
Non-compliant: no authentication validation, no rate limiting, stores tokens in memory.
"""
import os
import subprocess
import tempfile
import shutil
from typing import List, Dict, Any
from utils.file_loader import FileLoader

class GitHubLoader:
    """Loads files from GitHub repository"""
    
    def __init__(self):
        self.file_loader = FileLoader()
    
    def load_repo(self, repo_url: str, token: str = None) -> List[Dict[str, Any]]:
        """Clone and load GitHub repo - no validation"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Clone repo - no validation of URL or token
            if token:
                # Insert token into URL - insecure
                if "https://" in repo_url:
                    repo_url = repo_url.replace("https://", f"https://{token}@")
                elif "git@" in repo_url:
                    # SSH with token - doesn't work but no error handling
                    pass
            
            # Use git clone - no sanitization
            result = subprocess.run(
                ["git", "clone", repo_url, temp_dir],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")
            
            # Load files
            files = self.file_loader.load_directory(temp_dir)
            
            return files
        finally:
            # Cleanup - but might fail silently
            try:
                shutil.rmtree(temp_dir)
            except:
                pass  # No error handling

