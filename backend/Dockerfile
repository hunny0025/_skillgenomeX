FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Flask usually runs on 5000, but Gunicorn will bind to $PORT
ENV PORT=5000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT api:app"]
