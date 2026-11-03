# Docker Architecture — Air Quality Intelligence

## 1. Project Overview

Air Quality Intelligence is a machine-learning-based application designed to analyse air-quality measurements and estimate carbon monoxide (CO) concentration using user-provided inputs.

The application uses a Streamlit dashboard and an XGBoost machine learning model. Docker is used to package the application and its dependencies into a container for consistent execution.

## 2. System Architecture

```text
UCI Air Quality Dataset
          |
          v
Data Cleaning and Preprocessing
          |
          v
Trained XGBoost Model
          |
          v
Streamlit Dashboard
(dashboard/app.py)
          |
          v
Docker Image
air-quality-intelligence:latest
          |
          v
Docker Container
air-quality-app
          |
          v
Web Browser
http://localhost:8501
```

## 3. Docker Configuration

- Base image: Python 3.11 Slim
- Application framework: Streamlit
- Container port: 8501
- Host port: 8501
- Docker image name: air-quality-intelligence
- Container name: air-quality-app

## 4. Deployment Commands

**Build the Docker image:**

```bash
docker build -t air-quality-intelligence .
```

**Run the Docker container:**

```bash
docker run -d --name air-quality-app -p 8501:8501 air-quality-intelligence
```

**Verify the running container:**

```bash
docker ps --filter "name=air-quality-app"
```

The application can be accessed locally at:

http://localhost:8501

## 5. Current Implementation

The application has been successfully packaged into a Docker image and executed inside a