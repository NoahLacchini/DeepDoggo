#!/bin/bash

# Directory containing the input fastq files

INPUT_DIR="directory/cancer_final"

# Output directory

OUTPUT_DIR="directory/cancer_final"

# Loop through the fastq files
for file in ${INPUT_DIR}/.fastq; do
    # Extract the file name without extension
    filename=$(basename "$file")
    filename_no_ext="${filename%.}"

    # Construct the output file name
    output_file="${OUTPUT_DIR}/${filename_no_ext}.fasta"

    # Execute seqtk command
    seqtk seq -a "${file}" > "${output_file}"

    # Print status
    echo "Converted ${filename} to ${filename_no_ext}.fasta"
done
