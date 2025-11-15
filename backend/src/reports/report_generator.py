"""
Report generator - creates JSON and Markdown reports.
Non-compliant: no file permission checks, overwrites without backup.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any

class ReportGenerator:
    """Generates compliance reports"""
    
    def __init__(self):
        self.reports_dir = "reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)  # No permission check
    
    def generate(self, report_id: str, findings: List[Dict[str, Any]], score: Dict[str, Any], files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate report - no validation"""
        report = {
            "id": report_id,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_files_scanned": len(files),
                "total_findings": len(findings),
                "readiness_score": score.get("readiness_score", 0),
            },
            "score": score,
            "findings": findings,
            "controls": score.get("control_coverage", {}),
        }
        
        # Save JSON
        json_path = os.path.join(self.reports_dir, f"{report_id}.json")
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)  # No error handling
        
        # Save Markdown
        md_path = os.path.join(self.reports_dir, f"{report_id}.md")
        md_content = self._generate_markdown(report)
        with open(md_path, 'w') as f:
            f.write(md_content)  # No error handling
        
        report["report_path"] = json_path
        report["markdown_path"] = md_path
        
        return report
    
    def _generate_markdown(self, report: Dict[str, Any]) -> str:
        """Generate Markdown report"""
        md = f"""# SOC 2 Readiness Report

**Report ID:** {report['id']}  
**Generated:** {report['generated_at']}

## Summary

- **Readiness Score:** {report['summary']['readiness_score']}/100
- **Total Files Scanned:** {report['summary']['total_files_scanned']}
- **Total Findings:** {report['summary']['total_findings']}

## Score Breakdown

"""
        
        # Severity breakdown
        severity = report['score'].get('severity_breakdown', {})
        md += "### Severity Breakdown\n\n"
        for sev, count in severity.items():
            md += f"- **{sev.upper()}:** {count}\n"
        md += "\n"
        
        # Control coverage
        controls = report.get('controls', {})
        if controls:
            md += "### Control Coverage\n\n"
            for control_id, data in controls.items():
                md += f"- **{control_id}:** {data['findings']} findings\n"
            md += "\n"
        
        # Findings
        md += "## Findings\n\n"
        for finding in report['findings']:
            md += f"### {finding.get('type', 'Unknown')} - {finding.get('category', 'Unknown')}\n\n"
            md += f"- **Severity:** {finding.get('severity', 'Unknown')}\n"
            md += f"- **File:** `{finding.get('file', 'Unknown')}`\n"
            if finding.get('line'):
                md += f"- **Line:** {finding.get('line')}\n"
            md += f"- **Message:** {finding.get('message', 'No message')}\n"
            
            if finding.get('soc2_controls'):
                md += f"- **SOC 2 Controls:** {', '.join(finding.get('soc2_controls', []))}\n"
            
            if finding.get('explanation'):
                md += f"- **Explanation:** {finding.get('explanation')}\n"
            
            if finding.get('remediation'):
                md += f"- **Remediation:** {finding.get('remediation')}\n"
            
            md += "\n"
        
        return md

