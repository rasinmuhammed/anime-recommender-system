FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required for Python packages like h5py, numpy, tensorflow, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libatlas-base-dev \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    pkg-config \             
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip to ensure modern build compatibility
RUN pip install --upgrade pip

# Set the working directory inside the container
WORKDIR /app

# Copy the code into the container
COPY . .

# Install Python dependencies (editable mode for local project)
RUN pip install --no-cache-dir -e .

# (Optional) Train the model before running the app (or move to a separate stage in CI/CD)
RUN python pipeline/training_pipeline.py

# Expose the Flask app's port
EXPOSE 5001

# Default command to run the application
CMD ["python", "application.py"]
