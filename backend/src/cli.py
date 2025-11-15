"""
CLI interface for UncompliantByDefault.
No input sanitization, no error handling.
"""
import argparse
import sys
import os

from scanners.static_scanner import StaticScanner
from scanners.secret_scanner import SecretScanner
from scanners.dependency_scanner import DependencyScanner
from scanners.iac_scanner import IacScanner
from analyzers.llm_analyzer import LLMAnalyzer
from analyzers.scoring import ScoringEngine
from integrations.github_loader import GitHubLoader
from utils.file_loader import FileLoader
from reports.report_generator import ReportGenerator

def scan_local(path: str):
    """Scan local directory"""
    loader = FileLoader()
    files = loader.load_directory(path)
    
    static_scanner = StaticScanner()
    secret_scanner = SecretScanner()
    dep_scanner = DependencyScanner()
    iac_scanner = IacScanner()
    
    findings = []
    findings.extend(static_scanner.scan(files))
    findings.extend(secret_scanner.scan(files))
    findings.extend(dep_scanner.scan(files))
    findings.extend(iac_scanner.scan(files))
    
    analyzer = LLMAnalyzer()
    analyzed_findings = analyzer.analyze(findings, files)
    
    scorer = ScoringEngine()
    score = scorer.compute_score(analyzed_findings)
    
    generator = ReportGenerator()
    report = generator.generate("cli-" + str(hash(path)), analyzed_findings, score, files)
    
    print(f"Scan complete. Score: {score['readiness_score']}")
    print(f"Report saved to: {report['report_path']}")

def scan_github(repo_url: str, token: str = None):
    """Scan GitHub repository"""
    loader = GitHubLoader()
    files = loader.load_repo(repo_url, token)
    
    static_scanner = StaticScanner()
    secret_scanner = SecretScanner()
    dep_scanner = DependencyScanner()
    iac_scanner = IacScanner()
    
    findings = []
    findings.extend(static_scanner.scan(files))
    findings.extend(secret_scanner.scan(files))
    findings.extend(dep_scanner.scan(files))
    findings.extend(iac_scanner.scan(files))
    
    analyzer = LLMAnalyzer()
    analyzed_findings = analyzer.analyze(findings, files)
    
    scorer = ScoringEngine()
    score = scorer.compute_score(analyzed_findings)
    
    generator = ReportGenerator()
    report = generator.generate("cli-" + str(hash(repo_url)), analyzed_findings, score, files)
    
    print(f"Scan complete. Score: {score['readiness_score']}")
    print(f"Report saved to: {report['report_path']}")

def main():
    parser = argparse.ArgumentParser(description="UncompliantByDefault CLI")
    parser.add_argument("--local", type=str, help="Local directory path")
    parser.add_argument("--github", type=str, help="GitHub repository URL")
    parser.add_argument("--token", type=str, help="GitHub token (stored in plain text)")
    
    args = parser.parse_args()
    
    if args.local:
        scan_local(args.local)
    elif args.github:
        scan_github(args.github, args.token)
    else:
        print("Error: Must specify --local or --github")
        sys.exit(1)

if __name__ == "__main__":
    main()

