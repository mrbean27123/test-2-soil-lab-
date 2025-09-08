# ==================================================================================================
# Multi-stage Dockerfile for FastAPI Microservice
# Optimized for production with security, performance, and maintainability
# ==================================================================================================

# --------------------------------------------------------------------------------------------------
# BUILD STAGE: Compile dependencies and build artifacts
# This stage includes build tools and compilers that won't be in final image
# --------------------------------------------------------------------------------------------------
FROM python:3.12-slim as builder

# Set build-time environment variables
ENV PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install build dependencies required for compiling Python packages
# These include compilers and development headers needed for psycopg2, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for build stage
WORKDIR /build

# Copy requirements file to leverage Docker layer caching
# If requirements.txt hasn't changed, Docker will reuse the pip install layer
COPY requirements.txt .

# Install Python dependencies to user directory to avoid permission issues
# Using --user flag installs packages to ~/.local which we'll copy to runtime stage
RUN pip install --upgrade pip \
    && pip install --user --no-warn-script-location -r requirements.txt

# --------------------------------------------------------------------------------------------------
# RUNTIME STAGE: Final production image with minimal footprint
# This stage only contains runtime dependencies and application code
# --------------------------------------------------------------------------------------------------
FROM python:3.12-slim as runtime

# Metadata labels following OCI specification
LABEL maintainer="admin@steel.pl.ua" \
      description="FastAPI Microservice with PostgreSQL support" \
      version="0.1.0"

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    ALEMBIC_CONFIG=/usr/src/app/alembic.ini \
    PYTHONPATH=/usr/src/app/src \
    PATH=/home/appuser/.local/bin:$PATH

# Install only runtime dependencies (not development packages)
# libpq5: PostgreSQL client library (runtime only, no dev headers)
# netcat-openbsd: Network utility for health checks and service discovery
# postgresql-client: PostgreSQL command-line tools for database operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    postgresql-client \
    dos2unix \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Create non-root user for security best practices
# -r: create system user/group (lower UID/GID range)
# -m: create home directory
# -s /bin/bash: set default shell
RUN groupadd -r appuser && \
    useradd -r -g appuser -m -d /home/appuser -s /bin/bash appuser

# Set working directory and ensure proper ownership
WORKDIR /usr/src/app

# Copy Python packages from builder stage to user's local directory
# This includes all compiled dependencies without build tools
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code with proper ownership
# Using --chown during COPY is more efficient than separate chown command
COPY --chown=appuser:appuser . .

# Process shell scripts to ensure cross-platform compatibility
# Convert Windows line endings to Unix and make scripts executable
RUN find /usr/src/app -name "*.sh" -type f -exec dos2unix {} \; && \
    find /usr/src/app -name "*.sh" -type f -exec chmod +x {} \;

# Switch to non-root user for security
# All subsequent commands and the main process will run as this user
USER appuser

# Expose the port that FastAPI will run on
# This is documentation - actual port binding happens at runtime
EXPOSE 8000

# Add health check to monitor container status
# FastAPI typically serves health endpoint at /health or /docs
# Adjust the endpoint based on your application's health check route
# HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
#    CMD curl -f http://localhost:8000/health || exit 1

# Default command - can be overridden in docker-compose or kubernetes
# Using exec form to ensure proper signal handling
# CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["commands/run-app.sh"]
