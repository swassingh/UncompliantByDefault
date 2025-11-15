import { useRouter } from 'next/router'

export default function Navbar() {
  const router = useRouter()

  return (
    <nav style={{
      background: '#333',
      color: 'white',
      padding: '1rem 2rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <div
        onClick={() => router.push('/')}
        style={{ cursor: 'pointer', fontSize: '1.2rem', fontWeight: 'bold' }}
      >
        UncompliantByDefault
      </div>
      <div style={{ display: 'flex', gap: '1.5rem' }}>
        <a
          onClick={() => router.push('/')}
          style={{ cursor: 'pointer', textDecoration: 'none', color: 'white' }}
        >
          Home
        </a>
        <a
          onClick={() => router.push('/scan')}
          style={{ cursor: 'pointer', textDecoration: 'none', color: 'white' }}
        >
          Scan
        </a>
      </div>
    </nav>
  )
}

