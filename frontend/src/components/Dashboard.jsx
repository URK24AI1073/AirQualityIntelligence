
import './Dashboard.css'
import BackendStatus from './BackendStatus'

function Dashboard() {
  return (
    <div className="dashboard-page">
      <div className="dashboard-heading">
        <div>
          <span className="dashboard-label">
            AIR QUALITY INTELLIGENCE
          </span>
          <h1>Air Quality Dashboard</h1>
          <p>
            Explore environmental measurements and pollution trends.
          </p>
        </div>

        <span className="dashboard-status">
          <span className="status-dot"></span>
          Historical Dataset
        </span>
      </div>

      {/* Backend connection indicator */}
      <div style={{ marginBottom: '24px' }}>
        <BackendStatus />
      </div>

      <div className="dashboard-cards">
        <div className="metric-card">
          <span>Dataset</span>
          <h2>UCI Air Quality</h2>
          <small>Historical measurements</small>
        </div>

        <div className="metric-card">
          <span>ML Model</span>
          <h2>XGBoost</h2>
          <small>CO concentration estimation</small>
        </div>

        <div className="metric-card">
          <span>Analytics</span>
          <h2>Interactive</h2>
          <small>Pollution data visualisation</small>
        </div>
      </div>

      <div className="dashboard-panel">
        <h2>Pollution Analytics</h2>
        <p>
          This section will display pollution trends and interactive
          visualisations from the processed air-quality dataset.
        </p>

        <div className="chart-placeholder">
          <i className="bi bi-bar-chart-line"></i>
          <span>Air quality charts will appear here</span>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
