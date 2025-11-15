"""
Infrastructure as Code scanner.
Non-compliant: basic pattern matching, no proper IaC parsing.
"""
import re
import json
from typing import List, Dict, Any

class IacScanner:
    """Scans IaC files for misconfigurations"""
    
    def __init__(self):
        # Basic patterns - should use proper IaC parsers
        self.terraform_patterns = {
            "public_access": r'publicly_accessible\s*=\s*true',
            "no_encryption": r'encrypted\s*=\s*false',
            "weak_ssl": r'minimum_protocol_version\s*=\s*["\']TLSv1["\']',
        }
        
        self.cloudformation_patterns = {
            "public_access": r'PubliclyAccessible.*true',
            "no_encryption": r'Encrypted.*false',
        }
    
    def scan(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Scan IaC files"""
        findings = []
        
        iac_files = [f for f in files if any(ext in f.get("path", "").lower() for ext in [".tf", ".tfvars", ".yaml", ".yml", ".json"])]
        
        for file in iac_files:
            content = file.get("content", "")
            file_path = file.get("path", "")
            
            if ".tf" in file_path.lower():
                findings.extend(self._scan_terraform(content, file_path))
            elif "cloudformation" in file_path.lower() or "cfn" in file_path.lower():
                findings.extend(self._scan_cloudformation(content, file_path))
            elif "dockerfile" in file_path.lower():
                findings.extend(self._scan_dockerfile(content, file_path))
        
        return findings
    
    def _scan_terraform(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Scan Terraform files"""
        findings = []
        
        for category, pattern in self.terraform_patterns.items():
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                findings.append({
                    "type": "iac",
                    "category": category,
                    "severity": "high",
                    "file": file_path,
                    "line": content[:match.start()].count('\n') + 1,
                    "message": f"Terraform misconfiguration: {category}",
                })
        
        return findings
    
    def _scan_cloudformation(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Scan CloudFormation files"""
        findings = []
        
        try:
            data = json.loads(content) if content.strip().startswith('{') else None
            if data:
                # Basic checks
                if "Resources" in data:
                    for resource in data["Resources"].values():
                        if "Properties" in resource:
                            props = resource["Properties"]
                            if props.get("PubliclyAccessible") == True:
                                findings.append({
                                    "type": "iac",
                                    "category": "public_access",
                                    "severity": "high",
                                    "file": file_path,
                                    "message": "CloudFormation resource with public access enabled",
                                })
        except:
            pass  # No error handling
        
        return findings
    
    def _scan_dockerfile(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Scan Dockerfile"""
        findings = []
        
        # Check for root user
        if re.search(r'USER\s+root', content, re.IGNORECASE):
            findings.append({
                "type": "iac",
                "category": "root_user",
                "severity": "medium",
                "file": file_path,
                "message": "Dockerfile runs as root user",
            })
        
        # Check for exposed ports
        if re.search(r'EXPOSE\s+\d+', content):
            findings.append({
                "type": "iac",
                "category": "exposed_ports",
                "severity": "low",
                "file": file_path,
                "message": "Dockerfile exposes ports",
            })
        
        return findings

