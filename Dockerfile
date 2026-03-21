FROM python:3.12.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user and ensure instance dir is writable
RUN useradd -m -u 1000 appuser \
    && mkdir -p instance \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

ENV FLASK_ENV=production

CMD ["python", "app.py"]
