#!/bin/bash

# Test text to be converted to speech
TEST_TEXT="This is a test of the Text-to-Speech service running in Docker."

# Send request to TTS service
echo "Sending test request to TTS service..."
curl -X POST -H "Content-Type: application/json" \
     -d "{\"text\":\"$TEST_TEXT\"}" \
     --output test_tts_output.mp3 \
     http://localhost:5000/synthesize

# Check if the request was successful
if [ $? -eq 0 ]; then
    echo "Test successful. Audio file 'test_tts_output.mp3' has been created."
    echo "You can play this file to verify the audio output."
else
    echo "Test failed. Make sure the TTS service is running and accessible."
fi
