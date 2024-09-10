#!/bin/bash

# Check if the user provided the JSON file as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <input-json-file> [output-json-file]"
  exit 1
fi

# Check if such file exists
INPUT_JSON_FILE=$1

if [ ! -f "$INPUT_JSON_FILE" ]; then
  echo "File not found: $INPUT_JSON_FILE"
  exit 1
fi

URL="http://127.0.0.1:5000/check-grammar"

# Make post request and save response as json file (default name: output.json)
OUTPUT_JSON_FILE=${2:-output.json}

curl -s -X POST "$URL" \
     -H "Content-Type: application/json" \
     -d @"$INPUT_JSON_FILE" \
     -o "$OUTPUT_JSON_FILE"

echo "Response has been saved to $OUTPUT_JSON_FILE"

exit 0
