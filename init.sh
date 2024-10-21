#!/bin/bash

# Navigate to the TTS directory
cd tts

# Force rebuild of the Docker image
echo "Building TTS service Docker image..."
docker build -t tts-service -f Dockerfile .

# Remove any existing container
if [ "$(docker ps -aq -f name=tts-service)" ]; then
    echo "Removing existing TTS service container..."
    docker rm -f tts-service
fi

# Run the container
echo "Starting TTS service container..."
docker run -d -p 5000:5000 --name tts-service tts-service
echo "TTS service is now running."

# Return to the original directory
cd ..

echo "TTS service initialization complete."

# Add error handling for Dockerfile
if [ ! -f Dockerfile ]; then
    echo "Error: Dockerfile not found. Please ensure it exists in the current directory."
    exit 1
fi

# Add a check for the TTS service readiness
MAX_RETRIES=30
RETRY_INTERVAL=2

for i in $(seq 1 $MAX_RETRIES); do
    if curl -s http://localhost:5000/health > /dev/null; then
        echo "TTS service is ready."
        break
    fi
    if [ $i -eq $MAX_RETRIES ]; then
        echo "Error: TTS service failed to start after $MAX_RETRIES attempts."
        exit 1
    fi
    echo "Waiting for TTS service to be ready... (Attempt $i/$MAX_RETRIES)"
    sleep $RETRY_INTERVAL
done

# Test the TTS service with a curl request
echo "Testing TTS service with a curl request..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health

if [ $? -eq 0 ]; then
    echo "TTS service curl test passed."
else
    echo "Error: TTS service curl test failed."
    exit 1
fi

# Start the report script
echo "Starting report script..."
if ! python report.py; then
    echo "Error: The report script encountered an issue."
    echo "This might be due to a ChromeDriver version mismatch."
    echo "Please ensure that your Chrome/Chromium browser is up to date."
    echo "You can update ChromeDriver by running:"
    echo "pip install --upgrade webdriver-manager"
    echo "If the issue persists, you may need to manually download the correct ChromeDriver version from:"
    echo "https://sites.google.com/a/chromium.org/chromedriver/downloads"
    echo "and place it in your PATH."
    exit 1
fi

echo "Initialization and report generation complete."
