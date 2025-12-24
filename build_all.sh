#!/bin/bash
set -e

# This script builds all the Docker images for the labs.

echo "Building Docker images for all labs..."

# Build labs 01-10
for i in $(seq -f "%02g" 1 10); do
  LAB_DIR="labs/llm${i}_lab"
  IMAGE_NAME="llm${i}_lab"
  if [ -d "$LAB_DIR" ]; then
    echo "Building $IMAGE_NAME from $LAB_DIR..."
    sudo docker build -t "$IMAGE_NAME" "$LAB_DIR"
  else
    echo "Warning: Directory $LAB_DIR not found."
  fi
done

# Build labs 11-19
LAB_DIRS=$(find labs -maxdepth 1 -type d -name "llm[1-9][1-9]_*" | sort)
for LAB_DIR in $LAB_DIRS; do
  IMAGE_NAME=$(basename "$LAB_DIR")
  if [ -d "$LAB_DIR" ]; then
    echo "Building $IMAGE_NAME from $LAB_DIR..."
    sudo docker build -t "$IMAGE_NAME" "$LAB_DIR"
  else
    echo "Warning: Directory $LAB_DIR not found."
  fi
done


echo "All lab images built successfully."
