import { useState } from 'react'
import { useRouter } from 'next/router'
import Navbar from '@/components/Navbar'
import RepoSelector from '@/components/RepoSelector'
import ScanProgress from '@/components/ScanProgress'
import { scanLocal, scanGithub } from '@/lib/api'

export default function ScanPage() {
  const router = useRouter()
  const [scanType, setScanType] = useState<'local' | 'github' | null>(null)
  const [jobId, setJobId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleScan = async (type: 'local' | 'github', value: string, token?: string) => {
    try {
      setError(null)
      let id: string

      if (type === 'local') {
        id = await scanLocal(value)
      } else {
        id = await scanGithub(value, token)
      }

      setJobId(id)
      setScanType(type)
    } catch (err: any) {
      setError(err.message || 'Scan failed')
    }
  }

  const handleScanComplete = (reportId: string) => {
    router.push(`/report/${reportId}`)
  }

  return (
    <div>
      <Navbar />
      <main style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '2rem' }}>Scan Repository</h1>

        {!jobId ? (
          <>
            <RepoSelector onScan={handleScan} />
            {error && (
              <div style={{
                marginTop: '1rem',
                padding: '1rem',
                background: '#fee',
                color: '#c00',
                borderRadius: '4px'
              }}>
                Error: {error}
              </div>
            )}
          </>
        ) : (
          <ScanProgress jobId={jobId} onComplete={handleScanComplete} />
        )}
      </main>
    </div>
  )
}

