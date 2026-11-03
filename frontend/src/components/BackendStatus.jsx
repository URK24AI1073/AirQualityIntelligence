
import { useEffect, useState } from 'react'
import { checkBackendHealth } from '../services/api.js'

function BackendStatus() {
  const [status, setStatus] = useState('Checking connection...')

  useEffect(() => {
    async function checkConnection() {
      try {
        const data = await checkBackendHealth()

        setStatus(
          data.status === 'healthy'
            ? 'Backend Connected'
            : 'Backend Unavailable'
        )
      } catch (error) {
        setStatus('Backend Disconnected')
      }
    }

    checkConnection()
  }, [])

  const connected = status === 'Backend Connected'

  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '9px',
        padding: '10px 16px',
        borderRadius: '30px',
        background: connected ? '#e7f7ef' : '#fff3e8',
        color: connected ? '#147a49' : '#a45b16',
        fontWeight: 600,
        fontSize: '14px',
      }}
    >
      <span
        style={{
          width: '9px',
          height: '9px',
          borderRadius: '50%',
          background: connected ? '#16a05d' : '#e69a35',
        }}
      />
      {status}
    </div>
  )
}

export default BackendStatus
