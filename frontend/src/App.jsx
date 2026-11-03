
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'

import Home from './pages/Home'
import DashboardPage from './pages/DashboardPage'
import Analytics from './pages/Analytics'
import Prediction from './pages/Prediction'
import History from './pages/History'
import About from './pages/About'

import './App.css'

function Navigation() {
  return (
    <nav className="navbar">
      <NavLink to="/" className="brand">
        <span className="brand-icon">🌍</span>
        <span>
          AIR<span className="brand-highlight">QUALITY</span>
        </span>
      </NavLink>

      <div className="nav-links">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/dashboard">Dashboard</NavLink>
        <NavLink to="/analytics">Analytics</NavLink>
        <NavLink to="/prediction">Prediction</NavLink>
        <NavLink to="/history">History</NavLink>
        <NavLink to="/about">About</NavLink>
      </div>
    </nav>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Navigation />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/prediction" element={<Prediction />} />
        <Route path="/history" element={<History />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App