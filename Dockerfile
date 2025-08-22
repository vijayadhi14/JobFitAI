# Dockerfile for JobFit AI

# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir streamlit

# Expose ports: 8000 for FastAPI, 8501 for Streamlit
EXPOSE 8000
EXPOSE 8501

# Default command: start both backend and frontend
# Using simple background process for demo (production: use proper process manager)
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]
