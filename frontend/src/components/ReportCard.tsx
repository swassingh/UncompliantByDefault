interface ReportCardProps {
  report: {
    summary: {
      readiness_score: number
      total_findings: number
      total_files_scanned: number
    }
    score: {
      severity_breakdown: Record<string, number>
      control_coverage: Record<string, any>
    }
  }
}

export default function ReportCard({ report }: ReportCardProps) {
  const score = report.summary.readiness_score
  const scoreColor = score >= 80 ? '#0a0' : score >= 60 ? '#fa0' : '#c00'

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
      gap: '1.5rem',
      marginBottom: '2rem'
    }}>
      <div style={{
        background: '#f9f9f9',
        padding: '1.5rem',
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <h3 style={{ marginBottom: '0.5rem', color: '#666' }}>Readiness Score</h3>
        <div style={{
          fontSize: '3rem',
          fontWeight: 'bold',
          color: scoreColor
        }}>
          {score}
        </div>
        <div style={{ fontSize: '2rem', color: '#999' }}>/100</div>
      </div>

      <div style={{
        background: '#f9f9f9',
        padding: '1.5rem',
        borderRadius: '8px'
      }}>
        <h3 style={{ marginBottom: '1rem' }}>Severity Breakdown</h3>
        <div style={{ lineHeight: '2' }}>
          {Object.entries(report.score.severity_breakdown).map(([severity, count]) => (
            <div key={severity} style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ textTransform: 'capitalize' }}>{severity}:</span>
              <span style={{ fontWeight: 'bold' }}>{count}</span>
            </div>
          ))}
        </div>
      </div>

      <div style={{
        background: '#f9f9f9',
        padding: '1.5rem',
        borderRadius: '8px'
      }}>
        <h3 style={{ marginBottom: '1rem' }}>Summary</h3>
        <div style={{ lineHeight: '2' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Total Findings:</span>
            <span style={{ fontWeight: 'bold' }}>{report.summary.total_findings}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Files Scanned:</span>
            <span style={{ fontWeight: 'bold' }}>{report.summary.total_files_scanned}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Controls Affected:</span>
            <span style={{ fontWeight: 'bold' }}>{Object.keys(report.score.control_coverage).length}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

