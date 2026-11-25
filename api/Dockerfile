FROM python:3.11-slim
WORKDIR /srv
RUN pip install --no-cache-dir fastapi uvicorn psycopg[binary]
COPY app ./app
RUN useradd -m app
USER app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
