# Architecture Documentation

## System Overview

UncompliantByDefault is a full-stack application consisting of:

1. **Python FastAPI Backend** - REST API for scanning and analysis
2. **Next.js Frontend** - Web interface for users
3. **Google Gemini Integration** - AI-powered analysis

## Backend Architecture

### Components

#### API Layer (`api.py`)
- FastAPI router with REST endpoints
- Background task processing for scans
- In-memory job and report storage (non-compliant - should use database)

#### Scanners
- **StaticScanner**: Pattern-based code analysis
- **SecretScanner**: Detects API keys, passwords, tokens
- **DependencyScanner**: Checks for vulnerable packages
- **IacScanner**: Analyzes infrastructure as code files

#### Analyzers
- **LLMAnalyzer**: Uses Gemini to map findings to SOC 2 controls
- **ScoringEngine**: Computes readiness scores

#### Integrations
- **GitHubLoader**: Clones and loads GitHub repositories
- **FileLoader**: Loads files from local filesystem

#### Reports
- **ReportGenerator**: Creates JSON and Markdown reports

### Data Flow

1. User initiates scan (local or GitHub)
2. Files are loaded into memory
3. Multiple scanners run in parallel
4. Findings are collected
5. LLM analyzer maps findings to SOC 2 controls
6. Scoring engine computes readiness score
7. Report generator creates output files
8. Report stored and returned to user

## Frontend Architecture

### Pages
- **Index**: Landing page with product overview
- **Scan**: Repository selection and scan initiation
- **Report**: Detailed findings and score visualization

### Components
- Modular React components
- Client-side state management
- Polling-based progress updates

### API Client
- TypeScript API client (`lib/api.ts`)
- RESTful communication with backend
- Error handling (basic)

## Security Considerations

⚠️ **This application is intentionally non-compliant** and includes:

- No authentication or authorization
- No input validation
- No rate limiting
- Hardcoded secrets in code
- Insecure file operations
- No encryption for sensitive data
- Weak error handling
- No logging framework

## Deployment

### Backend
- Run with uvicorn or gunicorn
- Requires Gemini API key
- No database required (uses in-memory storage)

### Frontend
- Next.js production build
- Static export possible
- Requires backend API URL

## Future Improvements

For production use, implement:

1. Database for persistent storage
2. Authentication and authorization
3. Rate limiting
4. Input validation and sanitization
5. Proper logging and monitoring
6. Error recovery and retry logic
7. Secret management (vault, environment variables)
8. File size limits
9. Request timeout handling
10. CORS configuration

