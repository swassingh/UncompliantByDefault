# API Specification

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "ok"
}
```

---

### Scan Local Directory

**POST** `/scan/local`

Initiate a scan of a local directory.

**Request Body:**
```json
{
  "path": "/path/to/directory"
}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Status Codes:**
- `200 OK` - Scan job created
- `400 Bad Request` - Invalid request
- `500 Internal Server Error` - Server error

---

### Scan GitHub Repository

**POST** `/scan/github`

Initiate a scan of a GitHub repository.

**Request Body:**
```json
{
  "repo_url": "https://github.com/user/repo",
  "token": "ghp_xxx" // optional
}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Status Codes:**
- `200 OK` - Scan job created
- `400 Bad Request` - Invalid request
- `500 Internal Server Error` - Server error

---

### Get Job Status

**GET** `/job/{job_id}`

Get the status of a scan job.

**Response:**
```json
{
  "status": "running" | "completed" | "failed",
  "report_id": "550e8400-e29b-41d4-a716-446655440000", // if completed
  "error": "Error message" // if failed
}
```

**Status Codes:**
- `200 OK` - Job status retrieved
- `404 Not Found` - Job not found

---

### Get Report

**GET** `/report/{report_id}`

Get the full compliance report.

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "generated_at": "2024-01-15T10:30:00Z",
  "summary": {
    "total_files_scanned": 150,
    "total_findings": 23,
    "readiness_score": 72.5
  },
  "score": {
    "readiness_score": 72.5,
    "severity_breakdown": {
      "critical": 2,
      "high": 5,
      "medium": 10,
      "low": 6
    },
    "control_coverage": {
      "CC6.1": {
        "findings": 5,
        "severity_sum": 15
      },
      "CC6.2": {
        "findings": 3,
        "severity_sum": 8
      }
    },
    "total_findings": 23
  },
  "findings": [
    {
      "type": "secret",
      "category": "api_key",
      "severity": "critical",
      "file": "src/config.py",
      "line": 42,
      "message": "Potential api_key found",
      "secret_preview": "sk_live_1234567890...",
      "soc2_controls": ["CC6.1", "CC6.2"],
      "explanation": "Hardcoded API keys violate access control requirements...",
      "remediation": "Move API keys to environment variables or secret management system"
    }
  ],
  "controls": {
    "CC6.1": {
      "findings": 5,
      "severity_sum": 15
    }
  },
  "report_path": "reports/550e8400-e29b-41d4-a716-446655440000.json",
  "markdown_path": "reports/550e8400-e29b-41d4-a716-446655440000.md"
}
```

**Status Codes:**
- `200 OK` - Report retrieved
- `404 Not Found` - Report not found

---

## Data Models

### Finding

```typescript
interface Finding {
  type: string; // "static_analysis" | "secret" | "dependency" | "iac"
  category: string;
  severity: "critical" | "high" | "medium" | "low";
  file: string;
  line?: number;
  message: string;
  soc2_controls?: string[]; // Array of control IDs like ["CC6.1", "CC6.2"]
  explanation?: string;
  remediation?: string;
  // Additional fields based on type
}
```

### Score

```typescript
interface Score {
  readiness_score: number; // 0-100
  severity_breakdown: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  control_coverage: {
    [controlId: string]: {
      findings: number;
      severity_sum: number;
    };
  };
  total_findings: number;
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

**Common Status Codes:**
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Notes

- All scans run asynchronously in background tasks
- Poll `/job/{job_id}` to check scan status
- Reports are stored in-memory (non-persistent in current implementation)
- No authentication required (non-compliant)

