"""
Static code analysis scanner.
Intentionally non-compliant: no proper error handling, hardcoded patterns.
"""
import re
from typing import List, Dict, Any

class StaticScanner:
    """Scans code for static analysis patterns"""
    
    def __init__(self):
        # Hardcoded patterns - should be configurable
        self.patterns = {
            "hardcoded_secrets": [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
            ],
            "sql_injection": [
                r'execute\s*\(\s*["\'].*%.*["\']',
                r'query\s*\(\s*["\'].*%.*["\']',
            ],
            "no_authentication": [
                r'@app\.(get|post|put|delete)\(',
            ],
            "weak_crypto": [
                r'hashlib\.md5\(',
                r'hashlib\.sha1\(',
            ],
            "debug_code": [
                r'console\.log\(',
                r'print\s*\(',
                r'debugger',
            ],
        }
    
    def scan(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Scan files for patterns - no validation"""
        findings = []
        
        for file in files:
            content = file.get("content", "")
            file_path = file.get("path", "")
            
            for category, patterns in self.patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        findings.append({
                            "type": "static_analysis",
                            "category": category,
                            "severity": "high" if category in ["hardcoded_secrets", "sql_injection"] else "medium",
                            "file": file_path,
                            "line": content[:match.start()].count('\n') + 1,
                            "message": f"Found {category} pattern: {match.group()}",
                            "pattern": match.group(),
                        })
        
        return findings

