#!/bin/bash

# Navigate to the TTS directory
cd tts

# Check if the Docker image exists
if [[ "$(docker images -q tts-service 2> /dev/null)" == "" ]]; then
    echo "Building TTS service Docker image..."
    docker build -t tts-service -f Dockerfile .
else
    echo "TTS service Docker image already exists."
fi

# Check if the container is already running
if [ ! "$(docker ps -q -f name=tts-service)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=tts-service)" ]; then
        # Cleanup
        echo "Removing stopped TTS service container..."
        docker rm tts-service
    fi
    # Run the container
    echo "Starting TTS service container..."
    docker run -d -p 5000:5000 --name tts-service tts-service
    echo "TTS service is now running."
else
    echo "TTS service is already running."
fi

# Return to the original directory
cd ..

echo "TTS service initialization complete."

# Wait for the TTS service to be fully operational
echo "Waiting for TTS service to be ready..."
while ! curl -s http://localhost:5000/health > /dev/null; do
    sleep 1
done
echo "TTS service is ready."

# Start the report script
echo "Starting report script..."
#python report.py
