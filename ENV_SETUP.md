# Environment Variables Setup

This guide explains how to set up environment variables for UncompliantByDefault.

## Backend Environment Variables

Create a `.env` file in the `backend/` directory with the following:

```bash
# Required
GEMINI_API_KEY=your-gemini-api-key-here

# Optional
API_HOST=0.0.0.0
API_PORT=8000
```

### Getting a Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and paste it into your `.env` file

### Quick Setup

```bash
cd backend
# Copy the example file
cp env.example .env
# Edit .env and add your API key
```

## Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory with the following:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Quick Setup

```bash
cd frontend
# Copy the example file
cp env.example .env.local
# Edit .env.local if your backend runs on a different URL
```

## Environment Variable Reference

### Backend

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key for AI analysis |
| `API_HOST` | No | `0.0.0.0` | Host to bind the FastAPI server |
| `API_PORT` | No | `8000` | Port for the FastAPI server |

### Frontend

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | No | `http://localhost:8000` | Backend API base URL |

## Notes

- `.env` and `.env.local` files are gitignored and won't be committed
- Never commit API keys or secrets to version control
- For production, use proper secret management (e.g., AWS Secrets Manager, HashiCorp Vault)
- The `NEXT_PUBLIC_` prefix is required for Next.js to expose variables to the browser

