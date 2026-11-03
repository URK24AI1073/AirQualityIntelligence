
import './About.css'

function About() {
  const technologies = [
    {
      icon: 'bi-code-slash',
      name: 'React.js',
      description: 'Responsive frontend and interactive user interface',
    },
    {
      icon: 'bi-server',
      name: 'Node.js & Express',
      description: 'REST API development and backend integration',
    },
    {
      icon: 'bi-database',
      name: 'MongoDB Atlas',
      description: 'Cloud database for storing prediction records',
    },
    {
      icon: 'bi-robot',
      name: 'XGBoost',
      description: 'Machine learning regression for CO(GT) estimation',
    },
    {
      icon: 'bi-cloud',
      name: 'Cloud Computing',
      description: 'Cloud deployment and scalable data services',
    },
    {
      icon: 'bi-bar-chart',
      name: 'Python Analytics',
      description: 'Data preprocessing, analysis and model evaluation',
    },
    {
      icon: 'bi-diagram-3',
      name: 'FastAPI',
      description: 'Python API for serving machine learning predictions',
    },
    {
      icon: 'bi-box-seam',
      name: 'Docker',
      description: 'Containerization for application deployment',
    },
  ]

  const objectives = [
    'Analyse historical air-quality measurements.',
    'Clean and preprocess environmental datasets.',
    'Train an XGBoost regression model.',
    'Estimate carbon monoxide concentration using sensor inputs.',
    'Store prediction inputs and results in MongoDB.',
    'Present prediction records and model metrics through analytics.',
  ]

  return (
    <main className="about-page">
      <section className="about-hero">
        <span className="about-label">ABOUT OUR PROJECT</span>

        <h1>
          AIR QUALITY
          <br />
          <span>INTELLIGENCE</span>
        </h1>

        <p>
          A cloud-oriented air-quality analytics platform combining
          environmental data processing, machine learning and
          full-stack web technologies.
        </p>
      </section>

      <section className="about-content">
        <div className="about-section-heading">
          <span>PROJECT OVERVIEW</span>
          <h2>Turning Environmental Data into Insights</h2>
        </div>

        <p className="about-description">
          Air Quality Intelligence is an academic project that analyses
          historical air-pollution measurements and estimates carbon
          monoxide concentration using a trained XGBoost regression
          model. It integrates a React frontend, Node.js backend,
          FastAPI machine learning service and MongoDB database to
          provide an interactive prediction and analytics platform.
        </p>
      </section>

      <section className="technology-section">
        <div className="about-section-heading">
          <span>TECHNOLOGY STACK</span>
          <h2>Technologies Behind the Platform</h2>
          <p>
            Technologies currently integrated into the project and
            its supporting development workflow.
          </p>
        </div>

        <div className="technology-grid">
          {technologies.map(technology => (
            <article className="technology-card" key={technology.name}>
              <div className="technology-icon">
                <i className={`bi ${technology.icon}`}></i>
              </div>

              <h3>{technology.name}</h3>
              <p>{technology.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="about-content">
        <div className="about-section-heading">
          <span>PROJECT OBJECTIVES</span>
          <h2>What This Platform Aims to Achieve</h2>
        </div>

        <ul className="list-unstyled">
          {objectives.map((objective, index) => (
            <li className="d-flex gap-3 mb-3" key={index}>
              <i className="bi bi-check-circle-fill text-success"></i>
              <span>{objective}</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="about-objective">
        <div>
          <span>MACHINE LEARNING MODEL</span>
          <h2>XGBoost Regression</h2>

          <p>
            The trained model uses eight environmental sensor and
            atmospheric features to estimate CO(GT). Its evaluation
            on the held-out test set produced the following results:
          </p>

          <div className="row g-3 mt-3">
            <div className="col-4">
              <h3>0.2979</h3>
              <small>MAE</small>
            </div>

            <div className="col-4">
              <h3>0.5257</h3>
              <small>RMSE</small>
            </div>

            <div className="col-4">
              <h3>0.8673</h3>
              <small>R² Score</small>
            </div>
          </div>
        </div>

        <div className="objective-symbol">
          <i className="bi bi-globe-asia-australia"></i>
        </div>
      </section>

      <section className="about-content">
        <div className="about-section-heading">
          <span>DATASET AND SCOPE</span>
          <h2>Historical Air Quality Dataset</h2>
        </div>

        <p className="about-description">
          The project uses the UCI Air Quality dataset. The current
          model was trained using 6,139 training records and evaluated
          using 1,535 test records. It estimates CO(GT) from five
          sensor measurements, temperature, relative humidity and
          absolute humidity.
        </p>

        <p className="about-description">
          This implementation demonstrates predictions from supplied
          input values. It does not currently collect live sensor
          readings or provide real-time pollution monitoring.
        </p>
      </section>

      <footer className="about-footer">
        AIR QUALITY INTELLIGENCE © 2026
        <span>Data • Intelligence • Environment</span>
      </footer>
    </main>
  )
}

export default About
