#!/bin/bash

# Specify the directory containing the JSON files
directory=$1

# Check if the directory exists
if [ ! -d "$directory" ]; then
    echo "Directory $directory not found."
    exit 1
fi

# Delete JSON files in the directory
find "$directory" -type f -name "*.json" -delete

echo "JSON files deleted successfully."
