FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=300 --retries=10 -r requirements.txt

COPY ml_api.py .
COPY models/ ./models/
COPY reports/ ./reports/

EXPOSE 8000

CMD ["uvicorn", "ml_api:app", "--host", "0.0.0.0", "--port", "8000"]
