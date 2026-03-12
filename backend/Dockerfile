# Stage 1: Build stage
FROM python:3.11-slim AS build

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /app

# Copy only installed Python packages from build stage
COPY --from=build /install /usr/local

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
