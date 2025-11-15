import { useRouter } from 'next/router'
import Navbar from '@/components/Navbar'

export default function Home() {
  const router = useRouter()

  return (
    <div>
      <Navbar />
      <main style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
          UncompliantByDefault
        </h1>
        <p style={{ fontSize: '1.2rem', marginBottom: '2rem', color: '#666' }}>
          AI-Powered SOC 2 Readiness Agent
        </p>
        
        <div style={{ marginBottom: '3rem' }}>
          <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>What is SOC 2 Readiness?</h2>
          <p style={{ lineHeight: '1.6', marginBottom: '1rem' }}>
            SOC 2 (Service Organization Control 2) is a framework for managing data security. 
            Our tool analyzes your codebase to identify compliance gaps and provides actionable 
            recommendations to improve your SOC 2 readiness score.
          </p>
          <p style={{ lineHeight: '1.6' }}>
            We scan for security vulnerabilities, misconfigurations, and compliance issues 
            across your codebase, then use AI to map findings to specific SOC 2 controls.
          </p>
        </div>

        <div style={{ 
          background: '#f5f5f5', 
          padding: '2rem', 
          borderRadius: '8px',
          marginBottom: '2rem'
        }}>
          <h3 style={{ marginBottom: '1rem' }}>Features</h3>
          <ul style={{ lineHeight: '2' }}>
            <li>Static code analysis</li>
            <li>Secret detection</li>
            <li>Dependency vulnerability scanning</li>
            <li>Infrastructure as Code (IaC) analysis</li>
            <li>AI-powered SOC 2 control mapping</li>
            <li>Comprehensive reporting</li>
          </ul>
        </div>

        <button
          onClick={() => router.push('/scan')}
          style={{
            background: '#0070f3',
            color: 'white',
            border: 'none',
            padding: '1rem 2rem',
            fontSize: '1.1rem',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Scan Repository
        </button>
      </main>
    </div>
  )
}

