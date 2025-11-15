"""
FastAPI endpoints for SOC 2 scanning.
Intentionally non-compliant: no authentication, no rate limiting, no input validation.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uuid
import os
from datetime import datetime

from scanners.static_scanner import StaticScanner
from scanners.secret_scanner import SecretScanner
from scanners.dependency_scanner import DependencyScanner
from scanners.iac_scanner import IacScanner
from analyzers.llm_analyzer import LLMAnalyzer
from analyzers.scoring import ScoringEngine
from integrations.github_loader import GitHubLoader
from utils.file_loader import FileLoader
from reports.report_generator import ReportGenerator

router = APIRouter()

# In-memory storage - non-compliant, should use database
reports_store = {}
jobs_store = {}

class ScanLocalRequest(BaseModel):
    path: str

class ScanGithubRequest(BaseModel):
    repo_url: str
    token: Optional[str] = None  # No encryption - non-compliant

def run_scan(job_id: str, scan_type: str, target: str, token: Optional[str] = None):
    """Run full scan pipeline - no error handling, no logging"""
    try:
        # Load files
        if scan_type == "local":
            loader = FileLoader()
            files = loader.load_directory(target)
        else:
            loader = GitHubLoader()
            files = loader.load_repo(target, token)
        
        # Run scanners
        static_scanner = StaticScanner()
        secret_scanner = SecretScanner()
        dep_scanner = DependencyScanner()
        iac_scanner = IacScanner()
        
        findings = []
        findings.extend(static_scanner.scan(files))
        findings.extend(secret_scanner.scan(files))
        findings.extend(dep_scanner.scan(files))
        findings.extend(iac_scanner.scan(files))
        
        # Analyze with LLM
        analyzer = LLMAnalyzer()
        analyzed_findings = analyzer.analyze(findings, files)
        
        # Score
        scorer = ScoringEngine()
        score = scorer.compute_score(analyzed_findings)
        
        # Generate report
        generator = ReportGenerator()
        report = generator.generate(job_id, analyzed_findings, score, files)
        
        reports_store[job_id] = report
        jobs_store[job_id] = {"status": "completed", "report_id": job_id}
    except Exception as e:
        jobs_store[job_id] = {"status": "failed", "error": str(e)}

@router.post("/scan/local")
async def scan_local(request: ScanLocalRequest, background_tasks: BackgroundTasks):
    """Scan local directory - no path validation, no access control"""
    job_id = str(uuid.uuid4())
    jobs_store[job_id] = {"status": "running"}
    
    background_tasks.add_task(run_scan, job_id, "local", request.path)
    
    return {"job_id": job_id}

@router.post("/scan/github")
async def scan_github(request: ScanGithubRequest, background_tasks: BackgroundTasks):
    """Scan GitHub repo - no URL validation, token stored in plain text"""
    job_id = str(uuid.uuid4())
    jobs_store[job_id] = {"status": "running"}
    
    background_tasks.add_task(run_scan, job_id, "github", request.repo_url, request.token)
    
    return {"job_id": job_id}

@router.get("/report/{report_id}")
async def get_report(report_id: str):
    """Get report - no authorization check"""
    if report_id not in reports_store:
        raise HTTPException(status_code=404, detail="Report not found")
    return reports_store[report_id]

@router.get("/job/{job_id}")
async def get_job_status(job_id: str):
    """Get job status - no rate limiting"""
    if job_id not in jobs_store:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs_store[job_id]

@router.get("/health")
async def health():
    """Health check - no actual health validation"""
    return {"status": "ok"}

