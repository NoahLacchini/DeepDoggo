#!/bin/bash

# List of sample names
samples=(
"SAMPLE_NAMES"
)

# Directory paths
input_dir="directory/unmapped"
output_dir="directory/unmapped/sorted"

# Loop through each sample
for sample in "${samples[@]}"; do
    # Input and output file paths
    input_file="$input_dir/${sample}_bothEndsUnmapped.bam"
    output_file="$output_dir/${sample}_bothEndsUnmapped_sorted.bam"

    # Run the samtools sort command
    samtools sort -@3 -n "$input_file" -o "$output_file"

    # Print a message indicating completion for each sample
    echo "Sorting completed for $sample"

done
