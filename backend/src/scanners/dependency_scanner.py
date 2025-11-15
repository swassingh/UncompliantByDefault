"""
Dependency vulnerability scanner.
Non-compliant: no actual vulnerability database, hardcoded checks.
"""
import json
import re
from typing import List, Dict, Any

class DependencyScanner:
    """Scans dependencies for known vulnerabilities"""
    
    def __init__(self):
        # Hardcoded vulnerable packages - should use real CVE database
        self.vulnerable_packages = {
            "python": {
                "requests": ["<2.25.0"],
                "urllib3": ["<1.26.0"],
                "django": ["<3.2.0"],
            },
            "javascript": {
                "lodash": ["<4.17.21"],
                "axios": ["<0.21.1"],
            },
        }
    
    def scan(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Scan dependency files"""
        findings = []
        
        requirements_files = [f for f in files if "requirements.txt" in f.get("path", "").lower() or "package.json" in f.get("path", "").lower()]
        
        for file in requirements_files:
            content = file.get("content", "")
            file_path = file.get("path", "")
            
            if "requirements.txt" in file_path.lower():
                findings.extend(self._scan_python_deps(content, file_path))
            elif "package.json" in file_path.lower():
                findings.extend(self._scan_js_deps(content, file_path))
        
        return findings
    
    def _scan_python_deps(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Scan Python requirements.txt"""
        findings = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse package name and version
            match = re.match(r'([a-zA-Z0-9_-]+)([<>=!]+)?([0-9.]+)?', line)
            if match:
                package = match.group(1).lower()
                version = match.group(3) if match.group(3) else None
                
                if package in self.vulnerable_packages.get("python", {}):
                    vulnerable_versions = self.vulnerable_packages["python"][package]
                    findings.append({
                        "type": "dependency",
                        "category": "vulnerable_package",
                        "severity": "high",
                        "file": file_path,
                        "line": content.split('\n').index(line) + 1,
                        "message": f"Potentially vulnerable package: {package}",
                        "package": package,
                        "version": version,
                    })
        
        return findings
    
    def _scan_js_deps(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Scan package.json"""
        findings = []
        
        try:
            data = json.loads(content)
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            
            for package, version in deps.items():
                if package.lower() in self.vulnerable_packages.get("javascript", {}):
                    findings.append({
                        "type": "dependency",
                        "category": "vulnerable_package",
                        "severity": "high",
                        "file": file_path,
                        "message": f"Potentially vulnerable package: {package}",
                        "package": package,
                        "version": version,
                    })
        except:
            pass  # No error handling - non-compliant
        
        return findings

