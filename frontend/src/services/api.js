
const API_BASE_URL = 'http://localhost:5000'
const ML_API_URL = 'http://localhost:8000'

async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.message || data.detail || 'Request failed')
  }

  return data
}

export function checkBackendHealth() {
  return request(`${API_BASE_URL}/api/health`)
}

export function getPredictions() {
  return request(`${API_BASE_URL}/api/predictions`)
}

export function savePrediction(values) {
  return request(`${API_BASE_URL}/api/predictions`, {
    method: 'POST',
    body: JSON.stringify(values),
  })
}

export function deletePrediction(id) {
  return request(`${API_BASE_URL}/api/predictions/${id}`, {
    method: 'DELETE',
  })
}

export function predictAirQuality(values) {
  return request(`${ML_API_URL}/predict`, {
    method: 'POST',
    body: JSON.stringify(values),
  })
}