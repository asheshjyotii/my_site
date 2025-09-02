# Base image with Python
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies first for caching
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy Node.js dependencies for Tailwind/Flowbite
COPY package*.json /app/
RUN npm install

# Copy project files
COPY . /app/

# Build Tailwind CSS
RUN npm run build

# Collect static files
RUN python manage.py collectstatic --noinput


# Expose Django port
EXPOSE 8000

# Default command
CMD ["gunicorn", "main_site.wsgi:application", "--bind", "0.0.0.0:8000"]
