# Use a minimal official Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy required files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY main.py .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the app
CMD ["python", "main.py"]
