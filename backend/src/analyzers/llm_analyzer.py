"""
LLM Analyzer using Google Gemini.
Non-compliant: API key in environment, no rate limiting, no error recovery.
"""
import os
import google.generativeai as genai
from typing import List, Dict, Any
import yaml

class LLMAnalyzer:
    """Uses Gemini to analyze findings and map to SOC 2 controls"""
    
    def __init__(self):
        # API key from environment - no validation
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Load SOC 2 controls
        controls_path = os.path.join(os.path.dirname(__file__), "..", "config", "soc2_controls.yaml")
        with open(controls_path, 'r') as f:
            self.controls = yaml.safe_load(f)["soc2_controls"]
    
    def analyze(self, findings: List[Dict[str, Any]], files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze findings with LLM and map to SOC 2 controls"""
        analyzed = []
        
        # Batch findings for efficiency (but no actual batching - non-compliant)
        for finding in findings:
            prompt = self._build_prompt(finding)
            
            try:
                response = self.model.generate_content(prompt)
                analysis = self._parse_response(response.text, finding)
                analyzed.append(analysis)
            except Exception as e:
                # No error handling - just skip
                analyzed.append(finding)
        
        return analyzed
    
    def _build_prompt(self, finding: Dict[str, Any]) -> str:
        """Build prompt for Gemini"""
        controls_list = "\n".join([f"- {c['id']}: {c['name']}" for c in self.controls])
        
        return f"""Analyze this security finding and map it to relevant SOC 2 controls.

Finding:
- Type: {finding.get('type')}
- Category: {finding.get('category')}
- Severity: {finding.get('severity')}
- File: {finding.get('file')}
- Message: {finding.get('message')}

Available SOC 2 Controls:
{controls_list}

Provide:
1. List of relevant SOC 2 control IDs (comma-separated)
2. Brief explanation of why this finding relates to those controls
3. Recommended remediation steps

Format your response as:
CONTROLS: CC6.1, CC6.2
EXPLANATION: [your explanation]
REMEDIATION: [your remediation steps]
"""
    
    def _parse_response(self, response_text: str, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Parse LLM response - basic parsing, no validation"""
        finding = finding.copy()
        
        # Extract controls
        if "CONTROLS:" in response_text:
            controls_line = [l for l in response_text.split('\n') if 'CONTROLS:' in l][0]
            controls = [c.strip() for c in controls_line.split('CONTROLS:')[1].split(',')]
            finding['soc2_controls'] = controls
        else:
            finding['soc2_controls'] = []
        
        # Extract explanation
        if "EXPLANATION:" in response_text:
            explanation_lines = []
            in_explanation = False
            for line in response_text.split('\n'):
                if 'EXPLANATION:' in line:
                    in_explanation = True
                    explanation_lines.append(line.split('EXPLANATION:')[1].strip())
                elif in_explanation and ('REMEDIATION:' in line or line.strip() == ''):
                    break
                elif in_explanation:
                    explanation_lines.append(line.strip())
            finding['explanation'] = ' '.join(explanation_lines)
        else:
            finding['explanation'] = ""
        
        # Extract remediation
        if "REMEDIATION:" in response_text:
            remediation_lines = []
            in_remediation = False
            for line in response_text.split('\n'):
                if 'REMEDIATION:' in line:
                    in_remediation = True
                    remediation_lines.append(line.split('REMEDIATION:')[1].strip())
                elif in_remediation:
                    remediation_lines.append(line.strip())
            finding['remediation'] = ' '.join(remediation_lines)
        else:
            finding['remediation'] = ""
        
        return finding

