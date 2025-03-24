#!/bin/bash

INPUT_FILE="tests.txt"
OUTPUT_FILE="results.txt"
EXECUTABLE="python3 computor.py"  # Adjust this if your binary name is different

# Clear previous output
echo "ComputorV1 Test Results" > "$OUTPUT_FILE"
echo "=========================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

while IFS= read -r line
do
  # Skip empty lines or comments
  [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue

  echo "Input: $line" >> "$OUTPUT_FILE"
  $EXECUTABLE "$line" >> "$OUTPUT_FILE"
  echo "------------------------" >> "$OUTPUT_FILE"

done < "$INPUT_FILE"

echo "All results written to $OUTPUT_FILE"