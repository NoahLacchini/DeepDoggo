#!/bin/bash

output_file="output.txt"  # Replace with the desired output file name
n=50  # Replace with the desired size of each chunk

for input_file in fasta/*
do

  sequence=""

  # Read the input file line by line
  while IFS= read -r line
  do
    # Skip empty lines and header lines
    if [[ -z "$line" || $line == ">"* ]]; then
      
      # Split the genomic sequence into chunks of size n
      for (( i=0; (i+n)<${#sequence}; i+=n ))
      do
        chunk="${sequence:i:n}"
        echo "$chunk" >> "$output_file"  # Write the chunk to the output file
      done

      sequence=""

      continue
    fi

    # Concatenate the line with the previous line
    sequence="${sequence}${line}"

  done < "$input_file"  
      
  # Split the genomic sequence into chunks of size n
  for (( i=0; (i+n)<${#sequence}; i+=n ))
  do
    chunk="${sequence:i:n}"
    echo "$chunk" >> "$output_file"  # Write the chunk to the output file
  done
  
  echo "$input_file has been treated"  # Print a message indicating that the file has been processed

done
