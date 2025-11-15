# UncompliantByDefault Backend

AI-powered SOC 2 Readiness Agent - Backend Service

## Overview

This backend service provides REST API endpoints for scanning codebases and generating SOC 2 compliance reports. It uses Google Gemini for AI-powered analysis and multiple scanners to detect security issues.

## Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set environment variables:

```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

### Running the Server

Start the FastAPI server:

```bash
python -m uvicorn src.main:app --reload
```

Or use the main entry point:

```bash
python src/main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check

```
GET /health
```

Returns server status.

### Scan Local Directory

```
POST /scan/local
Content-Type: application/json

{
  "path": "/path/to/directory"
}
```

Returns:
```json
{
  "job_id": "uuid-string"
}
```

### Scan GitHub Repository

```
POST /scan/github
Content-Type: application/json

{
  "repo_url": "https://github.com/user/repo",
  "token": "optional-github-token"
}
```

Returns:
```json
{
  "job_id": "uuid-string"
}
```

### Get Job Status

```
GET /job/{job_id}
```

Returns:
```json
{
  "status": "running|completed|failed",
  "report_id": "uuid-string" // if completed
}
```

### Get Report

```
GET /report/{report_id}
```

Returns the full compliance report with findings, scores, and recommendations.

## CLI Usage

You can also use the CLI tool directly:

```bash
# Scan local directory
python src/cli.py --local /path/to/directory

# Scan GitHub repository
python src/cli.py --github https://github.com/user/repo --token ghp_xxx
```

## Architecture

- **Scanners**: Static analysis, secret detection, dependency scanning, IaC scanning
- **Analyzers**: LLM-powered analysis using Gemini, scoring engine
- **Integrations**: GitHub loader, file loader
- **Reports**: JSON and Markdown report generation

## Security Note

⚠️ **This codebase is intentionally non-compliant with SOC 2 standards** for demonstration purposes. Do not use in production without implementing proper security controls.

## Environment Variables

- `GEMINI_API_KEY`: Required. Your Google Gemini API key.

