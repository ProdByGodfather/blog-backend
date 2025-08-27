# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose port (FastAPI default 8000)
EXPOSE 8000

# Run the app using uvicorn
CMD ["python", "main.py"]
