# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR ./

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY ./app /app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run FastAPI using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
