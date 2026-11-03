
const mongoose = require('mongoose')

const predictionSchema = new mongoose.Schema(
  {
    pt08_s1_co: { type: Number, required: true },
    pt08_s2_nmhc: { type: Number, required: true },
    pt08_s3_nox: { type: Number, required: true },
    pt08_s4_no2: { type: Number, required: true },
    pt08_s5_o3: { type: Number, required: true },

    temperature: { type: Number, required: true },
    humidity: { type: Number, required: true },
    absolute_humidity: { type: Number, required: true },

    predictedCO: { type: Number, required: true },
    modelName: { type: String, default: 'XGBoost Regressor' },
  },
  { timestamps: true }
)

module.exports = mongoose.model('Prediction', predictionSchema)
