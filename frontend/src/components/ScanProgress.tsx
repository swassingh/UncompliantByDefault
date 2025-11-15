import { useEffect, useState } from 'react'
import { getJobStatus } from '@/lib/api'

interface ScanProgressProps {
  jobId: string
  onComplete: (reportId: string) => void
}

export default function ScanProgress({ jobId, onComplete }: ScanProgressProps) {
  const [status, setStatus] = useState<'running' | 'completed' | 'failed'>('running')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const pollStatus = async () => {
      try {
        const jobStatus = await getJobStatus(jobId)
        
        if (jobStatus.status === 'completed') {
          setStatus('completed')
          if (jobStatus.report_id) {
            onComplete(jobStatus.report_id)
          }
        } else if (jobStatus.status === 'failed') {
          setStatus('failed')
          setError(jobStatus.error || 'Scan failed')
        } else {
          // Continue polling
          setTimeout(pollStatus, 2000)
        }
      } catch (err: any) {
        setStatus('failed')
        setError(err.message || 'Failed to check status')
      }
    }

    pollStatus()
  }, [jobId, onComplete])

  return (
    <div style={{
      background: '#f9f9f9',
      padding: '2rem',
      borderRadius: '8px',
      textAlign: 'center',
      maxWidth: '600px'
    }}>
      {status === 'running' && (
        <>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⏳</div>
          <h2 style={{ marginBottom: '1rem' }}>Scanning Repository...</h2>
          <p style={{ color: '#666' }}>This may take a few minutes</p>
          <div style={{
            marginTop: '2rem',
            width: '100%',
            height: '4px',
            background: '#ddd',
            borderRadius: '2px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: '100%',
              height: '100%',
              background: '#0070f3',
              animation: 'pulse 2s infinite'
            }} />
          </div>
        </>
      )}

      {status === 'completed' && (
        <>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>✅</div>
          <h2 style={{ marginBottom: '1rem' }}>Scan Complete!</h2>
          <p>Redirecting to report...</p>
        </>
      )}

      {status === 'failed' && (
        <>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>❌</div>
          <h2 style={{ marginBottom: '1rem', color: '#c00' }}>Scan Failed</h2>
          <p style={{ color: '#c00' }}>{error}</p>
        </>
      )}

      <style jsx>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  )
}

