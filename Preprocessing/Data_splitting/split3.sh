#!/bin/bash

# Output file name
output_file="output2.txt"

# Clear the output file if it already exists
> "$output_file"

# Loop through each file in the fasta/ directory
for input_file in fasta/*; do
  # Extract file name without directory path
  file_name=$(basename "$input_file")

  # Initialize the chunk variable
  chunk=""

  # Open the input file and read the lines
  while IFS= read -r line; do

    if [[ $line == ">"* ]]; then
      continue
    fi

    # Remove line break characters from the line
    line="${line//$'\n'/}"

    # Iterate over each character in the line
    for (( i=0; i<${#line}; i++ )); do
      # Append the character to the chunk variable
      chunk+="${line:i:1}"

      # Check if the chunk has reached 50 characters
      if (( ${#chunk} == 50 )); then
        # Output the chunk to the output file
        echo "$chunk" >> "$output_file"

        # Reset the chunk variable
        chunk=""
      fi
    done
  done < "$input_file"

  # Add a line break to separate the content of each file
  echo >> "$output_file"
done
