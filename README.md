# UncompliantByDefault

AI-Powered SOC 2 Readiness Agent

> **Note**: This is a testing repository created for a hackathon (Part of the CompliantByDefault project). The codebase is intentionally non-compliant with SOC 2 standards for demonstration and educational purposes.

## Overview

UncompliantByDefault is a comprehensive tool for analyzing codebases and assessing SOC 2 compliance readiness. It combines static analysis, secret detection, dependency scanning, and AI-powered analysis to identify compliance gaps and provide actionable recommendations.

This project was developed as part of a hackathon to demonstrate AI-powered compliance analysis capabilities.

## Features

- 🔍 **Static Code Analysis** - Detects security patterns and anti-patterns
- 🔐 **Secret Detection** - Finds hardcoded credentials and API keys
- 📦 **Dependency Scanning** - Identifies vulnerable packages
- 🏗️ **IaC Analysis** - Scans infrastructure as code for misconfigurations
- 🤖 **AI-Powered Analysis** - Uses Google Gemini to map findings to SOC 2 controls
- 📊 **Comprehensive Reporting** - JSON and Markdown reports with scores and recommendations
- 🌐 **Web Interface** - Modern Next.js dashboard
- 🔧 **CLI Tool** - Command-line interface for automation
- 🔌 **REST API** - Programmatic access to scanning capabilities

## Project Structure

```
UncompliantByDefault/
├── backend/          # Python FastAPI backend
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── frontend/         # Next.js frontend
│   ├── src/
│   └── package.json
└── docs/            # Documentation
```

## Quick Start

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
export GEMINI_API_KEY="your-api-key"
python -m uvicorn src.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### CLI Usage

```bash
cd backend
python src/cli.py --local /path/to/repo
python src/cli.py --github https://github.com/user/repo
```

## Documentation

- [Architecture](docs/architecture.md) - System architecture and design
- [API Specification](docs/api_spec.md) - REST API documentation
- [Frontend Design](docs/frontend_design.md) - UI/UX documentation
- [Backend README](backend/README.md) - Backend setup and usage
- [Frontend README](frontend/README.md) - Frontend setup and usage

## Security Warning

⚠️ **IMPORTANT**: This codebase is **intentionally non-compliant** with SOC 2 standards for demonstration purposes. It includes:

- No authentication or authorization
- No input validation
- No rate limiting
- Hardcoded patterns and weak security practices
- Insecure file operations
- No proper error handling
- Missing logging and monitoring

**Do not use this code in production** without implementing proper security controls.

## Hackathon Project

This repository was created as a testing/demonstration project for a hackathon. It showcases:

- AI-powered code analysis using Google Gemini
- Multi-scanner security analysis
- SOC 2 compliance mapping
- Full-stack web application (FastAPI + Next.js)

The codebase intentionally includes non-compliant patterns to demonstrate what a SOC 2 readiness tool would detect.

## License

This project is for educational and demonstration purposes only.

