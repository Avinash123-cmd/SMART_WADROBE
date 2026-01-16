# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.10-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
ENV OPENCV_IO_MAX_IMAGE_PIXELS=1099511627776

WORKDIR /app

# Install runtime dependencies only (OpenCV runtime)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv

# Create non-root user
RUN useradd -m -u 1002 cvuser && \
    chown -R cvuser:cvuser /app
USER cvuser

# Copy application
COPY --chown=cvuser:cvuser . .

# Create data directory
RUN mkdir -p data && \
    chmod 755 data

# Expose port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Run Uvicorn with optimized settings
CMD ["uvicorn", \
    "main:app", \
    "--host", "0.0.0.0", \
    "--port", "8002", \
    "--workers", "2", \
    "--limit-concurrency", "50", \
    "--timeout-keep-alive", "30", \
    "--access-log", \
    "--log-level", "info"]