#!/bin/bash

# Set these variables
IMAGE_NAME="streamlit-cleared-cash-app"
VERSION="latest"
echo $HOST
echo $PORT
# Build the Docker image
docker buildx build --platform linux/arm64 --push -t $HOST:$PORT/$IMAGE_NAME:$VERSION .