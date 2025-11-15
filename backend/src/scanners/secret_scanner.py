"""
Secret scanning - detects API keys, passwords, tokens.
Non-compliant: uses weak regex, no false positive filtering.
"""
import re
from typing import List, Dict, Any

class SecretScanner:
    """Scans for secrets and credentials"""
    
    def __init__(self):
        # Weak patterns - should use proper secret detection libraries
        self.secret_patterns = {
            "aws_key": r'AKIA[0-9A-Z]{16}',
            "github_token": r'ghp_[a-zA-Z0-9]{36}',
            "private_key": r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----',
            "password": r'password["\s:=]+["\']?[^"\'\s]{8,}["\']?',
            "api_key": r'api[_-]?key["\s:=]+["\']?[a-zA-Z0-9]{20,}["\']?',
            "jwt": r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
        }
    
    def scan(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Scan for secrets - no validation"""
        findings = []
        
        for file in files:
            content = file.get("content", "")
            file_path = file.get("path", "")
            
            # Skip binary files
            if not isinstance(content, str):
                continue
            
            for secret_type, pattern in self.secret_patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    # No masking - exposes secrets in findings
                    secret_value = match.group()
                    findings.append({
                        "type": "secret",
                        "category": secret_type,
                        "severity": "critical",
                        "file": file_path,
                        "line": content[:match.start()].count('\n') + 1,
                        "message": f"Potential {secret_type} found",
                        "secret_preview": secret_value[:20] + "..." if len(secret_value) > 20 else secret_value,
                    })
        
        return findings

