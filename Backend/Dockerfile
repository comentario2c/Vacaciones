# Backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY Backend/ /app/

RUN pip install --upgrade pip && \
    pip install "fastapi[all]" && \
    pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]