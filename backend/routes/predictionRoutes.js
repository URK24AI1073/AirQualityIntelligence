
const express = require('express')
const Prediction = require('../models/Prediction')

const router = express.Router()

const requiredFields = [
  'pt08_s1_co',
  'pt08_s2_nmhc',
  'pt08_s3_nox',
  'pt08_s4_no2',
  'pt08_s5_o3',
  'temperature',
  'humidity',
  'absolute_humidity',
  'predictedCO',
]

router.get('/', async (req, res) => {
  try {
    const records = await Prediction.find().sort({ createdAt: -1 })

    res.json({
      success: true,
      count: records.length,
      data: records,
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      message: error.message,
    })
  }
})

router.post('/', async (req, res) => {
  try {
    const missingFields = requiredFields.filter(
      field =>
        req.body[field] === undefined ||
        req.body[field] === null ||
        req.body[field] === ''
    )

    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        message: 'Missing required fields.',
        missingFields,
      })
    }

    const values = {}

    for (const field of requiredFields) {
      values[field] = Number(req.body[field])

      if (!Number.isFinite(values[field])) {
        return res.status(400).json({
          success: false,
          message: `${field} must be a valid number.`,
        })
      }
    }

    if (values.humidity < 0 || values.humidity > 100) {
      return res.status(400).json({
        success: false,
        message: 'Humidity must be between 0 and 100.',
      })
    }

    const record = await Prediction.create(values)

    res.status(201).json({
      success: true,
      message: 'Prediction saved successfully.',
      data: record,
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      message: error.message,
    })
  }
})

router.delete('/:id', async (req, res) => {
  try {
    const deletedRecord = await Prediction.findByIdAndDelete(req.params.id)

    if (!deletedRecord) {
      return res.status(404).json({
        success: false,
        message: 'Prediction record not found.',
      })
    }

    res.json({
      success: true,
      message: 'Prediction deleted successfully.',
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      message: error.message,
    })
  }
})

module.exports = router
