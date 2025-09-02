# Multi-stage build optimized for Coolify
FROM node:18-alpine AS frontend-builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production --silent
COPY . .
RUN npm run build

FROM python:3.11-slim

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=main_site.settings
ENV PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN groupadd -r app && useradd -r -g app app

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy frontend assets from builder stage
COPY --from=frontend-builder /app/static ./static/
COPY --from=frontend-builder /app/node_modules ./node_modules/

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/logs

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Health check for Coolify
# HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
#     CMD curl -f http://localhost:${PORT:-8000}/health/ || exit 1

# Expose the port
EXPOSE ${PORT:-8000}

# Start the application
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn main_site.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 60 --keep-alive 2 --access-logfile - --error-logfile -"]