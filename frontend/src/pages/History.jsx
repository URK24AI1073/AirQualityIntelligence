
import { useEffect, useState } from 'react'
import { getPredictions, deletePrediction } from '../services/api.js'
import './History.css'

function History() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [deletingId, setDeletingId] = useState(null)

  async function loadHistory() {
    try {
      setLoading(true)
      setError('')

      const result = await getPredictions()
      setRecords(result.data || [])
    } catch (err) {
      setError(err.message || 'Unable to load records.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  async function handleDelete(id) {
    if (!window.confirm('Are you sure you want to delete this record?')) {
      return
    }

    try {
      setDeletingId(id)
      await deletePrediction(id)
      setRecords((previous) =>
        previous.filter((record) => record._id !== id)
      )
    } catch (err) {
      setError(err.message || 'Unable to delete record.')
    } finally {
      setDeletingId(null)
    }
  }

  async function clearHistory() {
    if (records.length === 0) return

    if (!window.confirm('Delete all displayed records permanently?')) {
      return
    }

    for (const record of records) {
      try {
        await deletePrediction(record._id)
      } catch (err) {
        setError(err.message || 'Unable to delete all records.')
        await loadHistory()
        return
      }
    }

    setRecords([])
  }

  function formatDate(value) {
    return new Date(value).toLocaleDateString('en-IN')
  }

  function formatTime(value) {
    return new Date(value).toLocaleTimeString('en-IN', {
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <main className="history-page">
      <div className="history-heading">
        <div>
          <span className="history-label">RECORD MANAGEMENT</span>
          <h1>Prediction History</h1>
          <p>Review saved air-quality measurement records.</p>
        </div>

        <button
          className="clear-history-button"
          onClick={clearHistory}
          disabled={records.length === 0 || loading}
        >
          <i className="bi bi-trash"></i>
          Clear Records
        </button>
      </div>

      <section className="history-summary">
        <div className="history-summary-card">
          <span>Total Records</span>
          <strong>{records.length}</strong>
          <small>Saved in database</small>
        </div>

        <div className="history-summary-card">
          <span>Record Source</span>
          <strong>MongoDB</strong>
          <small>Database records</small>
        </div>
      </section>

      <section className="history-table-panel">
        <div className="history-table-heading">
          <h2>Recent Records</h2>
          <span>{records.length} records</span>
        </div>

        {loading ? (
          <div className="history-empty">
            <p>Loading records...</p>
          </div>
        ) : error ? (
          <div className="history-empty">
            <p>{error}</p>
            <button onClick={loadHistory}>Try Again</button>
          </div>
        ) : records.length > 0 ? (
          <div className="history-table-wrapper">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Record ID</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Temperature</th>
                  <th>Humidity</th>
                  <th>CO</th>
                  <th>NO₂</th>
                  <th>Benzene</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {records.map((record) => (
                  <tr key={record._id}>
                    <td>#{record._id.slice(-6)}</td>
                    <td>{formatDate(record.createdAt)}</td>
                    <td>{formatTime(record.createdAt)}</td>
                    <td>{record.temperature}</td>
                    <td>{record.humidity}%</td>
                    <td>{record.co}</td>
                    <td>{record.no2}</td>
                    <td>{record.benzene}</td>
                    <td>
                      <button
                        type="button"
                        onClick={() => handleDelete(record._id)}
                        disabled={deletingId === record._id}
                        aria-label="Delete record"
                        title="Delete record"
                      >
                        <i className="bi bi-trash"></i>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="history-empty">
            <i className="bi bi-inbox"></i>
            <h3>No records available</h3>
            <p>Save a measurement from the Prediction page to see it here.</p>
          </div>
        )}
      </section>

      <p className="history-disclaimer">
        Records are retrieved from MongoDB. These are saved measurement
        inputs, not confirmed machine-learning predictions.
      </p>
    </main>
  )
}

export default History
