

# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the working directory
COPY script/ script/

# Copy the .env file to the container
COPY .env /app/.env

# Set environment variables from .env file
ENV $(cat /app/.env | xargs)

# Expose the port the application will run on
EXPOSE 8000

# Set environment variables for FastAPI
ENV HOST=0.0.0.0
ENV PORT=8000

# Start the application
CMD ["uvicorn", "script.main:app", "--host", "0.0.0.0", "--port", "8000"]
