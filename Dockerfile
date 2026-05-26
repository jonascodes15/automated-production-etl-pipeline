# Use a lightweight official Python image
FROM python:3.13.11-slim

# Set the active work room inside the container
WORKDIR /app

# Copy dependency configuration and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project code into the container
COPY . .

# Enable unbuffered Python output to ensure logs appear immediately
ENV PYTHONUNBUFFERED=1

# Run the pipeline when the container starts up
CMD ["python", "-u", "main.py"]