FROM python:3.12-slim

# ==========================
# Environment
# ==========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ==========================
# Create non-root user
# ==========================
RUN useradd -m appuser

# ==========================
# Working directory
# ==========================
WORKDIR /app

# ==========================
# Install dependencies
# ==========================
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ==========================
# Copy source code
# ==========================
COPY . .

# ==========================
# Change ownership
# ==========================
RUN chown -R appuser:appuser /app

USER appuser

# ==========================
# Expose port
# ==========================
EXPOSE 8000

# ==========================
# Run FastAPI
# ==========================
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "1", "-b", "0.0.0.0:8000"]