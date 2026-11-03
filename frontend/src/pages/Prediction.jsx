
import { useState } from 'react'
import {
  predictAirQuality,
  savePrediction,
} from '../services/api.js'

const initialValues = {
  pt08_s1_co: '',
  pt08_s2_nmhc: '',
  pt08_s3_nox: '',
  pt08_s4_no2: '',
  pt08_s5_o3: '',
  temperature: '',
  humidity: '',
  absolute_humidity: '',
}

const fields = [
  { name: 'pt08_s1_co', label: 'PT08.S1 (CO) sensor', step: 'any' },
  { name: 'pt08_s2_nmhc', label: 'PT08.S2 (NMHC) sensor', step: 'any' },
  { name: 'pt08_s3_nox', label: 'PT08.S3 (NOx) sensor', step: 'any' },
  { name: 'pt08_s4_no2', label: 'PT08.S4 (NO2) sensor', step: 'any' },
  { name: 'pt08_s5_o3', label: 'PT08.S5 (O3) sensor', step: 'any' },
  { name: 'temperature', label: 'Temperature (°C)', step: 'any' },
  { name: 'humidity', label: 'Relative humidity (%)', step: 'any' },
  { name: 'absolute_humidity', label: 'Absolute humidity', step: 'any' },
]

function Prediction() {
  const [values, setValues] = useState(initialValues)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)

  function handleChange(event) {
    const { name, value } = event.target

    setValues(previous => ({
      ...previous,
      [name]: value,
    }))

    setResult(null)
    setSaved(false)
    setError('')
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setLoading(true)
    setError('')
    setResult(null)
    setSaved(false)

    try {
      const input = {}

      for (const field of fields) {
        const value = Number(values[field.name])

        if (values[field.name].trim() === '' || !Number.isFinite(value)) {
          throw new Error(`Enter a valid value for ${field.label}.`)
        }

        input[field.name] = value
      }

      if (input.humidity < 0 || input.humidity > 100) {
        throw new Error('Relative humidity must be between 0 and 100.')
      }

      const predictionResponse = await predictAirQuality(input)

      if (!predictionResponse.success) {
        throw new Error('The ML model could not generate a prediction.')
      }

      setResult(predictionResponse)

      await savePrediction({
        ...input,
        predictedCO: predictionResponse.predicted_co,
      })

      setSaved(true)
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container py-5">
      <div className="mb-4">
        <h2 className="fw-bold">Air Quality Prediction</h2>
        <p className="text-muted">
          Enter the eight sensor measurements used by the trained XGBoost model.
        </p>
      </div>

      <div className="card border-0 shadow-sm rounded-4">
        <div className="card-body p-4">
          <form onSubmit={handleSubmit}>
            <div className="row g-4">
              {fields.map(field => (
                <div className="col-md-6" key={field.name}>
                  <label
                    htmlFor={field.name}
                    className="form-label fw-semibold"
                  >
                    {field.label}
                  </label>

                  <input
                    id={field.name}
                    name={field.name}
                    type="number"
                    step={field.step}
                    className="form-control"
                    value={values[field.name]}
                    onChange={handleChange}
                    required
                  />
                </div>
              ))}
            </div>

            <button
              type="submit"
              className="btn btn-primary mt-4 px-4"
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Predict Air Quality'}
            </button>
          </form>

          {error && (
            <div className="alert alert-danger mt-4" role="alert">
              {error}
            </div>
          )}

          {result && (
            <div className="alert alert-success mt-4">
              <h5 className="fw-bold">Prediction Result</h5>

              <p className="mb-1">
                Predicted CO(GT):
                <strong> {result.predicted_co} {result.unit}</strong>
              </p>

              <p className="mb-1">
                Model: {result.model}
              </p>

              <p className="mb-0">
                Target: {result.target}
              </p>

              {saved ? (
                <p className="mt-3 mb-0 fw-semibold">
                  <i className="bi bi-check-circle-fill me-2" />
                  Prediction saved successfully in MongoDB.
                </p>
              ) : (
                <p className="mt-3 mb-0">
                  Saving prediction to MongoDB...
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Prediction