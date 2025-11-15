import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Navbar from '@/components/Navbar'
import ReportCard from '@/components/ReportCard'
import FindingsTable from '@/components/FindingsTable'
import { getReport } from '@/lib/api'

interface Report {
  id: string
  generated_at: string
  summary: {
    total_files_scanned: number
    total_findings: number
    readiness_score: number
  }
  score: {
    readiness_score: number
    severity_breakdown: Record<string, number>
    control_coverage: Record<string, any>
    total_findings: number
  }
  findings: any[]
  controls: Record<string, any>
  report_path?: string
  markdown_path?: string
}

export default function ReportPage() {
  const router = useRouter()
  const { id } = router.query
  const [report, setReport] = useState<Report | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (id && typeof id === 'string') {
      loadReport(id)
    }
  }, [id])

  const loadReport = async (reportId: string) => {
    try {
      setLoading(true)
      const data = await getReport(reportId)
      setReport(data)
    } catch (err: any) {
      setError(err.message || 'Failed to load report')
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = (type: 'json' | 'markdown') => {
    if (!report) return

    if (type === 'json' && report.report_path) {
      // In production, this would fetch from backend
      window.open(`/api/download?path=${report.report_path}&type=json`, '_blank')
    } else if (type === 'markdown' && report.markdown_path) {
      window.open(`/api/download?path=${report.markdown_path}&type=md`, '_blank')
    }
  }

  if (loading) {
    return (
      <div>
        <Navbar />
        <main style={{ padding: '2rem', textAlign: 'center' }}>
          <p>Loading report...</p>
        </main>
      </div>
    )
  }

  if (error || !report) {
    return (
      <div>
        <Navbar />
        <main style={{ padding: '2rem', textAlign: 'center' }}>
          <p style={{ color: '#c00' }}>{error || 'Report not found'}</p>
        </main>
      </div>
    )
  }

  return (
    <div>
      <Navbar />
      <main style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem' }}>SOC 2 Readiness Report</h1>
          <div>
            <button
              onClick={() => handleDownload('json')}
              style={{
                marginRight: '0.5rem',
                padding: '0.5rem 1rem',
                background: '#666',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Download JSON
            </button>
            <button
              onClick={() => handleDownload('markdown')}
              style={{
                marginRight: '0.5rem',
                padding: '0.5rem 1rem',
                background: '#666',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Download Markdown
            </button>
            <button
              onClick={() => router.push('/scan')}
              style={{
                padding: '0.5rem 1rem',
                background: '#0070f3',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Re-run Scan
            </button>
          </div>
        </div>

        <div style={{ marginBottom: '2rem' }}>
          <p style={{ color: '#666' }}>
            Report ID: {report.id} | Generated: {new Date(report.generated_at).toLocaleString()}
          </p>
        </div>

        <ReportCard report={report} />

        <div style={{ marginTop: '3rem' }}>
          <h2 style={{ fontSize: '1.8rem', marginBottom: '1rem' }}>Findings</h2>
          <FindingsTable findings={report.findings} />
        </div>
      </main>
    </div>
  )
}

