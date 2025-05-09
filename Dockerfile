FROM python:3.8-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libatlas-base-dev \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    pkg-config \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY setup.py .
COPY requirements.txt* ./

# Install dependencies into a virtual environment
RUN python -m venv /venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install --no-cache-dir -e .

# Second stage: runtime image
FROM python:3.8-slim

# Copy virtual environment from builder stage
COPY --from=builder /venv /venv

# Set environment variables
ENV PATH="/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libatlas-base-dev \
    libhdf5-serial-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Expose the Flask app's port
EXPOSE 5001

# Default command
CMD ["python", "application.py"]