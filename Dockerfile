# Use a base image with Python and Node.js for building frontend
FROM python:3.11-slim

# Install Node.js + npm for frontend build
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs git && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy the whole project
COPY . .

# Optional: Install frontend dependencies if needed
# RUN cd frontend && npm install && npm run build
# But you're doing it with a Python script:
RUN python backend/build_frontend.py

# Install the Python backend package
RUN pip install .

# Set default command
CMD ["ee_review"]
