# Cloud-Based Air Quality Analytics and Pollution Prediction Using Machine Learning

## Project Overview
Air Quality Intelligence is a cloud-deployed analytics dashboard that explores air quality measurements and uses a trained XGBoost regression model to estimate carbon monoxide (CO) concentration from sensor measurements and environmental conditions.

## Objectives
- Analyze air quality sensor data.
- Visualize the distribution of CO measurements.
- Build a machine learning model to estimate CO concentration.
- Present model evaluation metrics in an interactive dashboard.
- Deploy the application online using Streamlit Community Cloud.

## Technologies Used
- Python
- Pandas and NumPy
- Scikit-learn
- XGBoost
- Plotly / Matplotlib
- Streamlit
- Git and GitHub

## Dataset
The project uses the UCI Air Quality dataset, containing sensor responses and environmental measurements.

Dataset source: https://archive.ics.uci.edu/dataset/360/air+quality

## Main Features
1. Dataset overview and measurement statistics.
2. Interactive CO distribution visualization.
3. CO prediction form using sensor and environmental inputs.
4. Model performance metrics: MAE, RMSE, and R².
5. Online dashboard deployment.

## Model Evaluation
The current dashboard reports:
- MAE: 0.2979
- RMSE: 0.5257
- R²: 0.8673

These values reflect the current evaluation setup and should be interpreted in the context of the dataset and train/test split.

## Run Locally
```bash
pip install -r requirements.txt
python -m streamlit run dashboard/app.py
```

## Limitations
The model estimates CO concentration from the supplied input measurements. It is not a verified future air-quality forecasting or public-health warning system.

## Future Enhancements
- Add time-based forecasting.
- Integrate live air quality data from a reliable API.
- Add cloud data storage and scheduled data processing.
- Expand visualizations for additional pollutants.
- Add model monitoring and retraining.

## Author
Student project — B.Tech Artificial Intelligence and Data Science
