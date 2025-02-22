# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy script file
COPY script.py .

# Create a volume to persist the output
VOLUME /app/output

# Set the entrypoint
ENTRYPOINT ["python", "script.py"]
