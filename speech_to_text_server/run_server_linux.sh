#!/bin/bash

# Speech-to-text server launcher for Linux
# This script runs the speech-to-text server that communicates with the BakkesMod plugin

# Default port (can be overridden with command line argument)
PORT=${1:-8003}

echo "Starting speech-to-text server on port $PORT..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the server
echo "Launching speech-to-text server..."
python speech-to-text-server.py $PORT 