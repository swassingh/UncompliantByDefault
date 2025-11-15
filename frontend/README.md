# UncompliantByDefault Frontend

Next.js frontend for the SOC 2 Readiness Agent

## Overview

Modern web interface for scanning repositories and viewing compliance reports.

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Environment Variables

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm start
```

## Pages

- `/` - Landing page with product overview
- `/scan` - Repository scanning interface
- `/report/[id]` - Detailed compliance report view

## Components

- `Navbar` - Navigation bar
- `RepoSelector` - Repository selection (GitHub or local)
- `ScanProgress` - Real-time scan progress indicator
- `ReportCard` - Summary card with readiness score
- `FindingsTable` - Sortable and filterable findings table

## API Integration

The frontend communicates with the backend via REST API. See `src/lib/api.ts` for API client implementation.

## Security Note

⚠️ **This codebase is intentionally non-compliant with SOC 2 standards** for demonstration purposes. Do not use in production without implementing proper security controls.

