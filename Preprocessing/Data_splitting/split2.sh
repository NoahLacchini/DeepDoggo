#!/bin/bash

# Output file name
output_file="output.txt"

# Clear the output file if it already exists
> "$output_file"

# Loop through each file in the fasta/ directory
for input_file in fasta/*; do
  # Extract file name without directory path
  file_name=$(basename "$input_file")

  # Processed content for the current file
  processed_content=$(tail -n +2 "$input_file" | tr -d '\n' | sed 's/.\{50\}/&\n/g')

  # Check if the last line has less than 50 characters
  last_line=$(echo "$processed_content" | tail -n 1)
  if [[ ${#last_line} -lt 50 ]]; then
    # Remove the last line
    processed_content=$(echo "$processed_content" | sed '$d')
  fi

  # Append the processed content to the output file
  echo -n "$processed_content" >> "$output_file"

  # Add a line break to separate the content of each file
  echo >> "$output_file"
done
