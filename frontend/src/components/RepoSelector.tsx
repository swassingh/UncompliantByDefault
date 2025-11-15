import { useState } from 'react'

interface RepoSelectorProps {
  onScan: (type: 'local' | 'github', value: string, token?: string) => void
}

export default function RepoSelector({ onScan }: RepoSelectorProps) {
  const [scanType, setScanType] = useState<'local' | 'github'>('github')
  const [githubUrl, setGithubUrl] = useState('')
  const [githubToken, setGithubToken] = useState('')
  const [localPath, setLocalPath] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (scanType === 'github') {
      if (!githubUrl) {
        alert('Please enter a GitHub URL')
        return
      }
      onScan('github', githubUrl, githubToken || undefined)
    } else {
      if (!localPath) {
        alert('Please select a local directory')
        return
      }
      onScan('local', localPath)
    }
  }

  return (
    <div style={{
      background: '#f9f9f9',
      padding: '2rem',
      borderRadius: '8px',
      maxWidth: '600px'
    }}>
      <h2 style={{ marginBottom: '1.5rem' }}>Select Repository</h2>

      <div style={{ marginBottom: '1.5rem' }}>
        <label style={{ display: 'block', marginBottom: '0.5rem' }}>
          <input
            type="radio"
            checked={scanType === 'github'}
            onChange={() => setScanType('github')}
            style={{ marginRight: '0.5rem' }}
          />
          GitHub Repository
        </label>
        <label style={{ display: 'block' }}>
          <input
            type="radio"
            checked={scanType === 'local'}
            onChange={() => setScanType('local')}
            style={{ marginRight: '0.5rem' }}
          />
          Local Directory
        </label>
      </div>

      <form onSubmit={handleSubmit}>
        {scanType === 'github' ? (
          <>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                GitHub URL
              </label>
              <input
                type="text"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                placeholder="https://github.com/user/repo"
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  fontSize: '1rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px'
                }}
              />
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                GitHub Token (Optional)
              </label>
              <input
                type="password"
                value={githubToken}
                onChange={(e) => setGithubToken(e.target.value)}
                placeholder="ghp_..."
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  fontSize: '1rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px'
                }}
              />
            </div>
          </>
        ) : (
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Local Directory Path
            </label>
            <input
              type="text"
              value={localPath}
              onChange={(e) => setLocalPath(e.target.value)}
              placeholder="C:\path\to\repo or /path/to/repo"
              style={{
                width: '100%',
                padding: '0.5rem',
                fontSize: '1rem',
                border: '1px solid #ddd',
                borderRadius: '4px'
              }}
            />
            <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem' }}>
              Note: For security reasons, enter the path manually. File picker requires additional setup.
            </p>
          </div>
        )}

        <button
          type="submit"
          style={{
            width: '100%',
            padding: '0.75rem',
            fontSize: '1.1rem',
            background: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Start Scan
        </button>
      </form>
    </div>
  )
}

