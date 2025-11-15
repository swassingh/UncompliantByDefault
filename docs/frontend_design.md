# Frontend Design Documentation

## Overview

The frontend is built with Next.js and React, providing a modern web interface for the SOC 2 Readiness Agent.

## Design Principles

- **Simple and Clean**: Minimalist UI focused on functionality
- **Responsive**: Works on desktop and mobile devices
- **Real-time Updates**: Polling-based progress tracking
- **Clear Visualizations**: Score cards and sortable tables

## Page Structure

### Landing Page (`/`)

**Purpose**: Introduce the product and guide users to start scanning

**Components**:
- Navbar
- Hero section with title and description
- Features list
- Call-to-action button

**Design**:
- Large, readable typography
- Clear value proposition
- Prominent "Scan Repository" button

### Scan Page (`/scan`)

**Purpose**: Allow users to select and scan a repository

**Components**:
- Navbar
- RepoSelector
- ScanProgress (shown after scan starts)

**Flow**:
1. User selects scan type (GitHub or local)
2. User provides repository path/URL
3. User optionally provides GitHub token
4. User clicks "Start Scan"
5. ScanProgress component shows status
6. On completion, redirects to report page

**Design**:
- Form-based input
- Clear radio button selection
- Real-time status updates
- Error messages displayed inline

### Report Page (`/report/[id]`)

**Purpose**: Display detailed compliance report

**Components**:
- Navbar
- ReportCard (summary with score)
- FindingsTable (detailed findings)

**Features**:
- Readiness score visualization
- Severity breakdown
- Sortable and filterable findings table
- Download buttons for JSON/Markdown
- Re-run scan button

**Design**:
- Score prominently displayed with color coding
- Grid layout for summary cards
- Full-width table for findings
- Action buttons in header

## Component Details

### Navbar

Simple navigation bar with:
- Logo/title (links to home)
- Navigation links (Home, Scan)

**Styling**: Dark background, white text

### RepoSelector

Form component for repository selection:
- Radio buttons for scan type
- Conditional input fields
- Submit button

**Validation**: Basic client-side validation (non-compliant - should validate on backend)

### ScanProgress

Real-time progress indicator:
- Animated spinner/loading state
- Status text
- Auto-redirects on completion

**Polling**: Polls backend every 2 seconds

### ReportCard

Summary visualization:
- Readiness score (large, color-coded)
- Severity breakdown
- Summary statistics

**Layout**: Grid of cards

### FindingsTable

Detailed findings display:
- Sortable columns (severity, file, type)
- Filterable by severity
- Color-coded severity badges
- SOC 2 control tags

**Features**:
- Responsive table with horizontal scroll
- Empty state message

## Styling Approach

- **Inline Styles**: Used throughout (non-compliant - should use CSS modules or styled-components)
- **Color Scheme**:
  - Primary: `#0070f3` (blue)
  - Critical: `#c00` (red)
  - High: `#f60` (orange)
  - Medium: `#fa0` (yellow)
  - Low: `#666` (gray)
- **Typography**: System fonts, clear hierarchy
- **Spacing**: Consistent padding and margins

## State Management

- **Local State**: React `useState` hooks
- **No Global State**: No Redux or Context API (simple enough for local state)
- **URL State**: Next.js router for navigation

## API Integration

- **Client**: `lib/api.ts` with fetch-based requests
- **Error Handling**: Basic try-catch blocks
- **Loading States**: Component-level loading indicators

## Responsive Design

- **Breakpoints**: Implicit (flexbox/grid adapts)
- **Mobile**: Stacked layouts, full-width buttons
- **Desktop**: Multi-column layouts, side-by-side components

## Accessibility

⚠️ **Non-compliant**: Missing:
- ARIA labels
- Keyboard navigation
- Screen reader support
- Focus management
- Color contrast validation

## Performance

- **Code Splitting**: Next.js automatic
- **Image Optimization**: Not applicable (no images)
- **Bundle Size**: Minimal dependencies

## Future Improvements

1. CSS modules or styled-components
2. Proper error boundaries
3. Loading skeletons
4. Toast notifications
5. Accessibility improvements
6. Dark mode
7. Export functionality
8. Charts/graphs for visualization
9. Search functionality
10. Pagination for large findings lists

