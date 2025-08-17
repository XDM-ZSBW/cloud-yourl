# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn for production WSGI server
RUN pip install --no-cache-dir gunicorn

# Copy application code
COPY app_simple.py .
COPY wsgi.py .
COPY templates/ ./templates/
COPY scripts/ ./scripts/

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the application using gunicorn with the WSGI entry point
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "120", "--keep-alive", "5", "wsgi:app"]
