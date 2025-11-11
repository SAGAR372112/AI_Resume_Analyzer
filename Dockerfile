# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . .

# Create static folder and add user (as root)
RUN mkdir -p /app/core/static \
    && adduser --disabled-password appuser \
    && chown -R appuser:appuser /app/core/static /app

# Copy entrypoint script (still as root)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user AFTER all root-level operations
USER appuser

# Expose Django port
EXPOSE 8000

# Start container with entrypoint
CMD ["/entrypoint.sh"]
