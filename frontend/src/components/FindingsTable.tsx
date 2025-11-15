import { useState } from 'react'

interface Finding {
  type: string
  category: string
  severity: string
  file: string
  line?: number
  message: string
  soc2_controls?: string[]
  explanation?: string
  remediation?: string
}

interface FindingsTableProps {
  findings: Finding[]
}

export default function FindingsTable({ findings }: FindingsTableProps) {
  const [sortBy, setSortBy] = useState<'severity' | 'file' | 'type'>('severity')
  const [filterSeverity, setFilterSeverity] = useState<string>('all')

  const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 }
  
  const sortedFindings = [...findings].sort((a, b) => {
    if (sortBy === 'severity') {
      return (severityOrder[a.severity as keyof typeof severityOrder] || 99) - 
             (severityOrder[b.severity as keyof typeof severityOrder] || 99)
    } else if (sortBy === 'file') {
      return a.file.localeCompare(b.file)
    } else {
      return a.type.localeCompare(b.type)
    }
  })

  const filteredFindings = filterSeverity === 'all' 
    ? sortedFindings 
    : sortedFindings.filter(f => f.severity === filterSeverity)

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return '#c00'
      case 'high': return '#f60'
      case 'medium': return '#fa0'
      case 'low': return '#666'
      default: return '#999'
    }
  }

  return (
    <div>
      <div style={{ marginBottom: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <label>
          Sort by:
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            style={{ marginLeft: '0.5rem', padding: '0.25rem' }}
          >
            <option value="severity">Severity</option>
            <option value="file">File</option>
            <option value="type">Type</option>
          </select>
        </label>
        <label>
          Filter:
          <select
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            style={{ marginLeft: '0.5rem', padding: '0.25rem' }}
          >
            <option value="all">All</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </label>
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          background: 'white',
          borderRadius: '8px',
          overflow: 'hidden'
        }}>
          <thead>
            <tr style={{ background: '#f5f5f5' }}>
              <th style={{ padding: '1rem', textAlign: 'left', borderBottom: '2px solid #ddd' }}>Severity</th>
              <th style={{ padding: '1rem', textAlign: 'left', borderBottom: '2px solid #ddd' }}>Type</th>
              <th style={{ padding: '1rem', textAlign: 'left', borderBottom: '2px solid #ddd' }}>File</th>
              <th style={{ padding: '1rem', textAlign: 'left', borderBottom: '2px solid #ddd' }}>Message</th>
              <th style={{ padding: '1rem', textAlign: 'left', borderBottom: '2px solid #ddd' }}>SOC 2 Controls</th>
            </tr>
          </thead>
          <tbody>
            {filteredFindings.map((finding, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '1rem' }}>
                  <span style={{
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    background: getSeverityColor(finding.severity),
                    color: 'white',
                    fontSize: '0.85rem',
                    fontWeight: 'bold',
                    textTransform: 'uppercase'
                  }}>
                    {finding.severity}
                  </span>
                </td>
                <td style={{ padding: '1rem' }}>{finding.type}</td>
                <td style={{ padding: '1rem', fontFamily: 'monospace', fontSize: '0.9rem' }}>
                  {finding.file}
                  {finding.line && <span style={{ color: '#666' }}>:{finding.line}</span>}
                </td>
                <td style={{ padding: '1rem' }}>{finding.message}</td>
                <td style={{ padding: '1rem' }}>
                  {finding.soc2_controls && finding.soc2_controls.length > 0 ? (
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem' }}>
                      {finding.soc2_controls.map((control, i) => (
                        <span
                          key={i}
                          style={{
                            padding: '0.2rem 0.4rem',
                            background: '#e3f2fd',
                            color: '#1976d2',
                            borderRadius: '4px',
                            fontSize: '0.85rem'
                          }}
                        >
                          {control}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span style={{ color: '#999' }}>—</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredFindings.length === 0 && (
        <div style={{ padding: '2rem', textAlign: 'center', color: '#666' }}>
          No findings found
        </div>
      )}
    </div>
  )
}

