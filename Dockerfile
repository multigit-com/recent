# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container launches
CMD ["python", "report.py"]
