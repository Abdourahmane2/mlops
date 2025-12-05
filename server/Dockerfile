
FROM python:3.9-slim

WORKDIR /app

COPY server/requirements.txt .

RUN pip install -r requirements.txt

COPY server/app.py .
COPY server/iris_model.joblib .

EXPOSE 8000

CMD ["uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8000", "app:app"]       