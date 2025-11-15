"""
Scoring engine for SOC 2 readiness.
Non-compliant: arbitrary scoring algorithm, no validation.
"""
from typing import List, Dict, Any

class ScoringEngine:
    """Computes SOC 2 readiness score"""
    
    def __init__(self):
        self.severity_weights = {
            "critical": 10,
            "high": 5,
            "medium": 2,
            "low": 1,
        }
    
    def compute_score(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compute readiness score - arbitrary formula"""
        if not findings:
            return {
                "readiness_score": 100,
                "control_coverage": {},
                "severity_breakdown": {},
            }
        
        # Count by severity
        severity_counts = {}
        for finding in findings:
            severity = finding.get("severity", "low")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Calculate penalty
        total_penalty = 0
        for severity, count in severity_counts.items():
            total_penalty += count * self.severity_weights.get(severity, 1)
        
        # Arbitrary formula - no validation
        base_score = 100
        penalty = min(total_penalty * 2, 80)  # Max 80 point penalty
        readiness_score = max(base_score - penalty, 0)
        
        # Control coverage
        control_coverage = {}
        for finding in findings:
            controls = finding.get("soc2_controls", [])
            for control in controls:
                if control not in control_coverage:
                    control_coverage[control] = {"findings": 0, "severity_sum": 0}
                control_coverage[control]["findings"] += 1
                control_coverage[control]["severity_sum"] += self.severity_weights.get(finding.get("severity", "low"), 1)
        
        return {
            "readiness_score": round(readiness_score, 2),
            "control_coverage": control_coverage,
            "severity_breakdown": severity_counts,
            "total_findings": len(findings),
        }

