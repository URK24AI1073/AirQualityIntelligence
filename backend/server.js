
const express = require('express')
const cors = require('cors')
const mongoose = require('mongoose')
require('dotenv').config()

const connectDB = require('./config/db')
const predictionRoutes = require('./routes/predictionRoutes')

const app = express()

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:5174',
}))

app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// Main route
app.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'Air Quality Intelligence API is running.',
    version: '1.0.0',
  })
})

// Health check
app.get('/api/health', (req, res) => {
  res.status(200).json({
    success: true,
    service: 'Air Quality Intelligence Backend',
    status: 'healthy',
    database: mongoose.connection.readyState === 1
      ? 'connected'
      : 'disconnected',
    timestamp: new Date().toISOString(),
  })
})

// Prediction API routes
app.use('/api/predictions', predictionRoutes)

// Handle unknown routes
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'API route not found.',
  })
})

// Global error handler
app.use((err, req, res, next) => {
  console.error('Server error:', err.message)

  res.status(500).json({
    success: false,
    message: 'Internal server error.',
  })
})

// Start server after database connection
async function startServer() {
  try {
    await connectDB()

    const PORT = process.env.PORT || 5000

    app.listen(PORT, () => {
      console.log(`Air Quality API running at http://localhost:${PORT}`)
      console.log(`Health check: http://localhost:${PORT}/api/health`)
      console.log(`Predictions API: http://localhost:${PORT}/api/predictions`)
    })
  } catch (error) {
    console.error('Unable to start server:', error.message)
    process.exit(1)
  }
}

startServer()
