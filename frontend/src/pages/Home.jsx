
import '../App.css'

function Home() {
  return (
    <div className="app">
      <main id="home" className="hero-section">
        <div className="hero-content">
          <span className="eyebrow">
            SMART ENVIRONMENTAL INTELLIGENCE
          </span>

          <h1>
            Understand the Air.
            <br />
            <span>Predict a Better Future.</span>
          </h1>

          <p>
            Explore air quality analytics and machine learning-powered
            pollution estimation through one intelligent platform.
          </p>

          <div className="hero-actions">
            <a href="/dashboard" className="primary-button">
              Explore Dashboard ↗
            </a>

            <a href="/about" className="secondary-button">
              Learn More
            </a>
          </div>

          <div className="hero-note">
            <span className="status-dot"></span>
            DATA-DRIVEN ENVIRONMENTAL ANALYSIS
          </div>
        </div>

        <div className="hero-visual">
          <div className="visual-circle">
            <span className="visual-icon">🌿</span>
            <div className="orbit orbit-one"></div>
            <div className="orbit orbit-two"></div>
          </div>

          <div className="floating-card">
            <span>AI-POWERED</span>
            <strong>Air Quality Analytics</strong>
            <small>Insights from environmental data</small>
          </div>
        </div>
      </main>

      <section id="features" className="features-section">
        <div className="section-heading">
          <span>OUR PLATFORM</span>
          <h2>Intelligence for Cleaner Air</h2>
          <p>
            Tools to explore, understand and estimate air pollution.
          </p>
        </div>

        <div className="feature-grid">
          <article className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Air Quality Analytics</h3>
            <p>
              Explore pollution measurements through interactive charts.
            </p>
          </article>

          <article className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>ML Prediction</h3>
            <p>
              Estimate carbon monoxide concentration using machine learning.
            </p>
          </article>

          <article className="feature-card">
            <div className="feature-icon">☁️</div>
            <h3>Cloud Platform</h3>
            <p>
              Access the application through its cloud-hosted deployment.
            </p>
          </article>
        </div>
      </section>

      <section id="about" className="about-section">
        <span>ABOUT THE PROJECT</span>
        <h2>Turning Environmental Data into Useful Insights</h2>
        <p>
          Air Quality Intelligence combines data analytics, machine learning
          and web technologies to make historical air pollution data easier
          to explore and understand.
        </p>
      </section>

      <footer>
        AIR QUALITY INTELLIGENCE © 2026
        <span>Built for a smarter, cleaner future.</span>
      </footer>
    </div>
  )
}

export default Home